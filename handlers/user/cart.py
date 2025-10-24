# handlers/user/cart.py
"""
Savat (cart) bilan ishlash: ko'rish, o'chirish, buyurtma berish
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.db import (
    get_user, get_cart_items, remove_from_cart,
    clear_cart, create_order, get_admins
)
from keyboards.user_keyboards import (
    get_cart_keyboard,
    get_payment_keyboard,
    get_phone_request_keyboard,
    get_back_to_main_menu_keyboard
)
from utils.localization import get_text

cart_router = Router()


# FSM uchun holatlar
class OrderStates(StatesGroup):
    waiting_for_phone = State()
    waiting_for_address = State()
    waiting_for_payment = State()


@cart_router.message(F.text.in_(['🛒 Savat', '🛒 Корзина']))
async def show_cart(message: Message):
    """
    Savatni ko'rsatish
    """
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get('language', 'uz')

    cart_items = await get_cart_items(user_id, lang)

    if not cart_items:
        await message.answer(
            get_text('cart_empty', lang),
            reply_markup=get_back_to_main_menu_keyboard(lang)
        )
        return

    # Har bir mahsulot uchun inline keyboard yaratish
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    for idx, item in enumerate(cart_items, 1):
        item_text = f"📦 {item['name']}\n\n"
        item_text += f"💰 Narxi: {item['price']:,.0f} {get_text('sum', lang)}\n"
        item_text += f"🔢 Miqdor: {item['quantity']} ta\n"
        item_text += f"💵 Jami: {item['price'] * item['quantity']:,.0f} {get_text('sum', lang)}"

        # Har bir mahsulot uchun o'chirish tugmasi
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_text('decrease_quantity', lang),
                    callback_data=f"cart_decrease_{item['cart_id']}"
                ),
                InlineKeyboardButton(
                    text=f"🔢 {item['quantity']}",
                    callback_data=f"cart_quantity_{item['cart_id']}"
                ),
                InlineKeyboardButton(
                    text=get_text('increase_quantity', lang),
                    callback_data=f"cart_increase_{item['cart_id']}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_text('remove_from_cart', lang),
                    callback_data=f"remove_cart_{item['cart_id']}"
                )
            ]
        ])

        await message.answer(item_text, reply_markup=keyboard)

    # Umumiy ma'lumot va harakatlar
    total = sum(item['price'] * item['quantity'] for item in cart_items)

    summary_text = f"\n{'=' * 30}\n"
    summary_text += f"📊 {get_text('cart_summary', lang)}\n\n"
    summary_text += f"📦 {get_text('total_items', lang)}: {len(cart_items)} ta\n"
    summary_text += f"💵 {get_text('total', lang)}: {total:,.0f} {get_text('sum', lang)}"

    await message.answer(
        summary_text,
        reply_markup=get_cart_keyboard(lang)
    )


@cart_router.callback_query(F.data.startswith("cart_increase_"))
async def increase_cart_quantity(callback: CallbackQuery):
    """
    Savat mahsuloti miqdorini oshirish
    """
    cart_item_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id

    user = await get_user(user_id)
    lang = user.get('language', 'uz')

    from database.db import update_cart_quantity
    result = await update_cart_quantity(cart_item_id, user_id, 1)  # +1

    if result:
        # Yangilangan ma'lumotni ko'rsatish
        from database.db import get_cart_item_by_id
        item = await get_cart_item_by_id(cart_item_id, user_id, lang)

        if item:
            item_text = f"📦 {item['name']}\n\n"
            item_text += f"💰 Narxi: {item['price']:,.0f} {get_text('sum', lang)}\n"
            item_text += f"🔢 Miqdor: {item['quantity']} ta\n"
            item_text += f"💵 Jami: {item['price'] * item['quantity']:,.0f} {get_text('sum', lang)}"

            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=get_text('decrease_quantity', lang),
                        callback_data=f"cart_decrease_{item['cart_id']}"
                    ),
                    InlineKeyboardButton(
                        text=f"🔢 {item['quantity']}",
                        callback_data=f"cart_quantity_{item['cart_id']}"
                    ),
                    InlineKeyboardButton(
                        text=get_text('increase_quantity', lang),
                        callback_data=f"cart_increase_{item['cart_id']}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=get_text('remove_from_cart', lang),
                        callback_data=f"remove_cart_{item['cart_id']}"
                    )
                ]
            ])

            await callback.message.edit_text(item_text, reply_markup=keyboard)

        await callback.answer(get_text('quantity_increased', lang))
    else:
        await callback.answer(get_text('cart_error', lang), show_alert=True)


@cart_router.callback_query(F.data.startswith("cart_decrease_"))
async def decrease_cart_quantity(callback: CallbackQuery):
    """
    Savat mahsuloti miqdorini kamaytirish
    """
    cart_item_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id

    user = await get_user(user_id)
    lang = user.get('language', 'uz')

    from database.db import update_cart_quantity, get_cart_item_by_id

    # Avval joriy miqdorni tekshirish
    item = await get_cart_item_by_id(cart_item_id, user_id, lang)

    if not item:
        await callback.answer(get_text('cart_error', lang), show_alert=True)
        return

    # Agar miqdor 1 ta bo'lsa, o'chirish
    if item['quantity'] <= 1:
        result = await remove_from_cart(cart_item_id, user_id)
        if result:
            await callback.message.delete()
            await callback.answer(get_text('removed_from_cart', lang))
        else:
            await callback.answer(get_text('cart_error', lang), show_alert=True)
        return

    # Miqdorni kamaytirish
    result = await update_cart_quantity(cart_item_id, user_id, -1)  # -1

    if result:
        # Yangilangan ma'lumotni ko'rsatish
        item = await get_cart_item_by_id(cart_item_id, user_id, lang)

        if item:
            item_text = f"📦 {item['name']}\n\n"
            item_text += f"💰 Narxi: {item['price']:,.0f} {get_text('sum', lang)}\n"
            item_text += f"🔢 Miqdor: {item['quantity']} ta\n"
            item_text += f"💵 Jami: {item['price'] * item['quantity']:,.0f} {get_text('sum', lang)}"

            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=get_text('decrease_quantity', lang),
                        callback_data=f"cart_decrease_{item['cart_id']}"
                    ),
                    InlineKeyboardButton(
                        text=f"🔢 {item['quantity']}",
                        callback_data=f"cart_quantity_{item['cart_id']}"
                    ),
                    InlineKeyboardButton(
                        text=get_text('increase_quantity', lang),
                        callback_data=f"cart_increase_{item['cart_id']}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=get_text('remove_from_cart', lang),
                        callback_data=f"remove_cart_{item['cart_id']}"
                    )
                ]
            ])

            await callback.message.edit_text(item_text, reply_markup=keyboard)

        await callback.answer(get_text('quantity_decreased', lang))
    else:
        await callback.answer(get_text('cart_error', lang), show_alert=True)


@cart_router.callback_query(F.data.startswith("remove_cart_"))
async def remove_from_cart_handler(callback: CallbackQuery):
    """
    Mahsulotni savatdan o'chirish
    Format: remove_cart_<cart_item_id>
    """
    cart_item_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id

    user = await get_user(user_id)
    lang = user.get('language', 'uz')

    result = await remove_from_cart(cart_item_id, user_id)

    if result:
        await callback.answer(get_text('removed_from_cart', lang))

        # Savatni yangilangan holda ko'rsatish
        cart_items = await get_cart_items(user_id, lang)

        if not cart_items:
            await callback.message.edit_text(
                get_text('cart_empty', lang),
                reply_markup=None
            )
            return

        # Yangilangan savatni ko'rsatish
        cart_text = get_text('cart_title', lang) + "\n\n"
        total = 0

        for idx, item in enumerate(cart_items, 1):
            cart_text += f"{idx}. {item['name']}\n"
            cart_text += f"   💰 {item['price']:,.0f} {get_text('sum', lang)} x {item['quantity']}\n"
            cart_text += f"   = {item['price'] * item['quantity']:,.0f} {get_text('sum', lang)}\n\n"
            total += item['price'] * item['quantity']

        cart_text += f"\n💵 {get_text('total', lang)}: {total:,.0f} {get_text('sum', lang)}"

        await callback.message.edit_text(
            cart_text,
            reply_markup=get_cart_keyboard(lang)
        )
    else:
        await callback.answer(get_text('cart_error', lang), show_alert=True)


@cart_router.callback_query(F.data == "clear_cart")
async def clear_cart_handler(callback: CallbackQuery):
    """
    Savatni tozalash
    """
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get('language', 'uz')

    result = await clear_cart(user_id)

    if result:
        await callback.message.edit_text(
            get_text('cart_cleared', lang),
            reply_markup=None
        )

    await callback.answer()


@cart_router.callback_query(F.data == "checkout")
async def start_checkout(callback: CallbackQuery, state: FSMContext):
    """
    Buyurtma berish jarayonini boshlash
    """
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    await callback.message.edit_text(
        get_text('send_phone', lang),
        reply_markup=None
    )

    await callback.message.answer(
        get_text('phone_request', lang),
        reply_markup=get_phone_request_keyboard(lang)
    )

    await state.set_state(OrderStates.waiting_for_phone)
    await callback.answer()


@cart_router.message(OrderStates.waiting_for_phone, F.contact)
async def process_phone(message: Message, state: FSMContext):
    """
    Telefon raqamini qabul qilish
    """
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'uz')

    phone = message.contact.phone_number
    await state.update_data(phone=phone)

    await message.answer(
        get_text('send_address', lang),
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(OrderStates.waiting_for_address)


@cart_router.message(OrderStates.waiting_for_address, F.text)
async def process_address(message: Message, state: FSMContext):
    """
    Manzilni qabul qilish
    """
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'uz')

    address = message.text
    await state.update_data(address=address)

    await message.answer(
        get_text('select_payment', lang),
        reply_markup=get_payment_keyboard(lang)
    )

    await state.set_state(OrderStates.waiting_for_payment)


@cart_router.callback_query(OrderStates.waiting_for_payment, F.data.startswith("payment_"))
async def process_payment(callback: CallbackQuery, state: FSMContext):
    """
    To'lov turini tanlash va buyurtmani yakunlash
    Format: payment_<type> (cash, click, payme)
    """
    payment_type = callback.data.split("_")[1]
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get('language', 'uz')

    # State dan ma'lumotlarni olish
    data = await state.get_data()
    phone = data.get('phone')
    address = data.get('address')

    # Savat mahsulotlarini olish
    cart_items = await get_cart_items(user_id, lang)
    total = sum(item['price'] * item['quantity'] for item in cart_items)

    # Buyurtma yaratish
    order = await create_order(
        user_id=user_id,
        phone=phone,
        address=address,
        payment_type=payment_type,
        cart_items=cart_items,
        total=total
    )

    if order:
        # Foydalanuvchiga xabar
        order_text = get_text('order_created', lang).format(
            order_id=order['id'],
            total=f"{total:,.0f}"
        )

        await callback.message.edit_text(order_text, reply_markup=None)

        # Savatni tozalash
        await clear_cart(user_id)

        # Adminga va operatorlar guruhiga xabar yuborish
        admin_text = f"🆕 Yangi buyurtma #{order['id']}\n\n"
        admin_text += f"👤 {callback.from_user.full_name}\n"
        admin_text += f"📞 {phone}\n"
        admin_text += f"📍 {address}\n"
        admin_text += f"💳 {payment_type.upper()}\n\n"
        admin_text += "📦 Mahsulotlar:\n"

        for idx, item in enumerate(cart_items, 1):
            admin_text += f"{idx}. {item['name']} x {item['quantity']} = {item['price'] * item['quantity']:,.0f} so'm\n"

        admin_text += f"\n💵 Jami: {total:,.0f} so'm"

        # Inline keyboard - operator qabul qilishi uchun
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        operator_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Qabul qilish",
                    callback_data=f"operator_accept_{order['id']}"
                )
            ]
        ])

        # Adminga yuborish
        admins = await get_admins()
        for admin_id in admins:
            try:
                await callback.bot.send_message(admin_id, admin_text)
            except Exception as e:
                print(f"❌ Admin ga yuborishda xatolik: {e}")

        # Operatorlar guruhiga yuborish
        from config import OPERATORS_GROUP_ID
        if OPERATORS_GROUP_ID:
            try:
                await callback.bot.send_message(
                    OPERATORS_GROUP_ID,
                    admin_text,
                    reply_markup=operator_keyboard
                )
            except Exception as e:
                print(f"❌ Operatorlar guruhiga yuborishda xatolik: {e}")

        await state.clear()

    else:
        await callback.answer(get_text('order_error', lang), show_alert=True)

    await callback.answer()