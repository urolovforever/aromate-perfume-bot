# handlers/admin/operator.py
"""
Operatorlar uchun handlerlar - buyurtmalarni qabul qilish va boshqarish
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest

from database.db import get_order_by_id, assign_operator_to_order, update_order_status, reduce_product_stock
from utils.localization import get_text
from utils.decorators import can_modify_order

operator_router = Router()


@operator_router.callback_query(F.data.startswith("operator_accept_"))
async def operator_accept_order(callback: CallbackQuery):
    """
    Operator buyurtmani qabul qiladi
    """
    order_id = int(callback.data.split("_")[2])
    operator_id = callback.from_user.id
    operator_username = callback.from_user.username or callback.from_user.full_name

    # Buyurtmani olish
    order = await get_order_by_id(order_id)

    if not order:
        await callback.answer("❌ Buyurtma topilmadi", show_alert=True)
        return

    # Agar allaqachon boshqa operator qabul qilgan bo'lsa
    if order.get('operator_id'):
        await callback.answer(
            f"⚠️ Bu buyurtma allaqachon {order['operator_username']} tomonidan qabul qilingan!",
            show_alert=True
        )
        return

    # Operatorni tayinlash
    result = await assign_operator_to_order(order_id, operator_id, operator_username)

    if result:
        # Xabarni yangilash - operator uchun status o'zgartirish tugmalari
        try:
            new_text = callback.message.text + f"\n\n✅ Qabul qildi: @{operator_username}"

            # Operator uchun status o'zgartirish klaviaturasi
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⏳ Jarayonga olish",
                        callback_data=f"op_status_{order_id}_processing"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🚚 Yetkazilmoqda",
                        callback_data=f"op_status_{order_id}_delivering"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="✅ Yakunlandi",
                        callback_data=f"op_status_{order_id}_completed"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Bekor qilish",
                        callback_data=f"op_status_{order_id}_cancelled"
                    )
                ]
            ])

            await callback.message.edit_text(
                new_text,
                reply_markup=keyboard
            )
        except TelegramBadRequest:
            pass

        await callback.answer(
            f"✅ Buyurtma #{order_id} sizga biriktirildi!",
            show_alert=True
        )
    else:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@operator_router.callback_query(F.data.startswith("op_status_"))
async def operator_change_status(callback: CallbackQuery):
    """
    Operator buyurtma statusini o'zgartiradi (guruhdan)
    Format: op_status_<order_id>_<new_status>
    """
    data = callback.data.split("_")
    order_id = int(data[2])
    new_status = data[3]
    operator_id = callback.from_user.id

    # Buyurtmani olish
    order = await get_order_by_id(order_id)

    if not order:
        await callback.answer("❌ Buyurtma topilmadi", show_alert=True)
        return

    # Operator huquqini tekshirish
    has_permission = await can_modify_order(operator_id, order.get('operator_id'))

    if not has_permission:
        await callback.answer(
            "❌ Siz faqat o'zingiz qabul qilgan buyurtmalarni boshqara olasiz!",
            show_alert=True
        )
        return

    # Statusni yangilash
    result = await update_order_status(order_id, new_status)

    if result:
        # Agar buyurtma yakunlangan bo'lsa, ombor miqdorini kamaytirish
        if new_status == 'completed':
            for item in order['items']:
                # Faqat bottle (asosiy mahsulot) uchun ombor miqdorini kamaytirish
                # ML variantlar uchun ombor kuzatilmaydi
                variant_type = item.get('variant_type', 'bottle')
                if variant_type == 'bottle':
                    await reduce_product_stock(item['product_id'], item['quantity'])

            # Kam qolgan mahsulotlarni tekshirish va adminlarga xabar berish
            from handlers.admin.inventory import check_and_notify_low_stock
            await check_and_notify_low_stock(callback.bot, 'uz')

        status_emoji = {
            'new': '🆕',
            'processing': '⏳',
            'delivering': '🚚',
            'completed': '✅',
            'cancelled': '❌'
        }

        status_text = {
            'new': 'Yangi',
            'processing': 'Jarayonda',
            'delivering': 'Yetkazilmoqda',
            'completed': 'Yakunlandi',
            'cancelled': 'Bekor qilindi'
        }

        # Xabarni yangilash
        try:
            lines = callback.message.text.split('\n')
            # Birinchi qatorni yangilash
            lines[0] = f"{status_emoji[new_status]} Buyurtma #{order_id} - {status_text[new_status]}"
            new_text = '\n'.join(lines)

            # Agar yakunlangan yoki bekor qilingan bo'lsa, klaviaturani olib tashlash
            if new_status in ['completed', 'cancelled']:
                await callback.message.edit_text(
                    new_text,
                    reply_markup=None
                )
            else:
                # Statusga mos klaviatura
                keyboard = get_operator_status_keyboard(order_id, new_status)
                await callback.message.edit_text(
                    new_text,
                    reply_markup=keyboard
                )
        except TelegramBadRequest:
            pass

        await callback.answer(
            f"✅ Status o'zgartirildi: {status_text[new_status]}",
            show_alert=True
        )
    else:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


def get_operator_status_keyboard(order_id: int, current_status: str) -> InlineKeyboardMarkup:
    """
    Joriy statusga mos klaviatura yaratish
    """
    buttons = []

    if current_status == 'new':
        buttons.append([
            InlineKeyboardButton(
                text="⏳ Jarayonga olish",
                callback_data=f"op_status_{order_id}_processing"
            )
        ])

    if current_status == 'processing':
        buttons.append([
            InlineKeyboardButton(
                text="🚚 Yetkazilmoqda",
                callback_data=f"op_status_{order_id}_delivering"
            )
        ])

    if current_status == 'delivering':
        buttons.append([
            InlineKeyboardButton(
                text="✅ Yakunlandi",
                callback_data=f"op_status_{order_id}_completed"
            )
        ])

    # Har doim bekor qilish imkoniyati
    if current_status not in ['completed', 'cancelled']:
        buttons.append([
            InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data=f"op_status_{order_id}_cancelled"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)