# handlers/admin/inventory.py
"""
Admin ombor boshqaruvi handlerlari
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.db import (
    get_user, get_all_products, update_product_stock,
    get_low_stock_products, get_out_of_stock_products,
    add_ml_variant, get_ml_variants, delete_ml_variant,
    get_product_by_id
)
from utils.localization import get_text
from utils.decorators import admin_only

inventory_router = Router()


class InventoryStates(StatesGroup):
    """Ombor boshqaruvi uchun holatlar"""
    waiting_for_stock = State()
    waiting_for_ml_amount = State()
    waiting_for_ml_price = State()


@inventory_router.callback_query(F.data == "manage_inventory")
@admin_only
async def manage_inventory_menu(callback: CallbackQuery):
    """
    Ombor boshqaruvi menyusi
    """
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    text = get_text('manage_inventory', lang) + "\n\n"
    text += "Quyidagi amallardan birini tanlang:" if lang == 'uz' else "Выберите одно из действий:"

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=get_text('admin_products_list', lang),
                callback_data="inventory_products_list"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text('check_low_stock', lang),
                callback_data="check_low_stock"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text('back', lang),
                callback_data="back_to_admin"
            )
        ]
    ])

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@inventory_router.callback_query(F.data == "inventory_products_list")
@admin_only
async def show_inventory_products(callback: CallbackQuery):
    """
    Mahsulotlar ro'yxatini ombor ma'lumotlari bilan ko'rsatish
    """
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    products = await get_all_products()

    if not products:
        await callback.answer(get_text('no_products', lang), show_alert=True)
        return

    text = get_text('products_list_title', lang) + "\n\n"

    buttons = []
    for product in products:
        stock_emoji = "✅" if product['stock_quantity'] > 5 else "⚠️" if product['stock_quantity'] > 0 else "❌"
        button_text = f"{stock_emoji} {product['name_uz']} ({product['stock_quantity']} dona)"
        buttons.append([
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"inventory_product_{product['id']}"
            )
        ])

    # Orqaga qaytish
    buttons.append([
        InlineKeyboardButton(
            text=get_text('back', lang),
            callback_data="manage_inventory"
        )
    ])

    from aiogram.types import InlineKeyboardMarkup
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@inventory_router.callback_query(F.data.startswith("inventory_product_"))
@admin_only
async def show_product_inventory(callback: CallbackQuery):
    """
    Mahsulot ombor ma'lumotlarini ko'rsatish
    """
    product_id = int(callback.data.split("_")[2])

    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    product = await get_product_by_id(product_id, lang)

    if not product:
        await callback.answer(get_text('product_not_found', lang), show_alert=True)
        return

    # ML variantlarni olish
    ml_variants = await get_ml_variants(product_id)

    text = f"🎁 {product['name']}\n\n"
    text += f"📦 {get_text('in_stock', lang)}: {product['stock_quantity']} {get_text('pieces', lang)}\n"
    text += f"💰 {get_text('enter_price', lang).replace(':', '')}: {product['price']:,.0f} {get_text('sum', lang)}\n"

    if ml_variants:
        text += f"\n💧 ML Variantlar:\n"
        for variant in ml_variants:
            text += f"  • {variant['ml_amount']} ML - {variant['price']:,.0f} {get_text('sum', lang)}\n"

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    buttons = [
        [
            InlineKeyboardButton(
                text=get_text('update_stock', lang),
                callback_data=f"update_stock_{product_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text('add_ml_variant', lang),
                callback_data=f"add_ml_variant_{product_id}"
            )
        ]
    ]

    # ML variantlarni o'chirish tugmalari
    if ml_variants:
        for variant in ml_variants:
            buttons.append([
                InlineKeyboardButton(
                    text=f"🗑 {variant['ml_amount']} ML ni o'chirish",
                    callback_data=f"delete_ml_{variant['id']}"
                )
            ])

    buttons.append([
        InlineKeyboardButton(
            text=get_text('back', lang),
            callback_data="inventory_products_list"
        )
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@inventory_router.callback_query(F.data.startswith("update_stock_"))
@admin_only
async def start_update_stock(callback: CallbackQuery, state: FSMContext):
    """
    Ombor miqdorini yangilash jarayonini boshlash
    """
    product_id = int(callback.data.split("_")[2])

    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    await state.update_data(product_id=product_id, lang=lang)
    await state.set_state(InventoryStates.waiting_for_stock)

    await callback.message.edit_text(get_text('enter_new_stock', lang))
    await callback.answer()


@inventory_router.message(InventoryStates.waiting_for_stock)
@admin_only
async def process_update_stock(message: Message, state: FSMContext):
    """
    Yangi ombor miqdorini qabul qilish va yangilash
    """
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    product_id = data.get('product_id')

    try:
        new_stock = int(message.text)

        if new_stock < 0:
            await message.answer("❌ Miqdor 0 dan katta bo'lishi kerak")
            return

        result = await update_product_stock(product_id, new_stock)

        if result:
            await message.answer(get_text('stock_updated', lang))

            # Kam qolgan mahsulotlarni tekshirish
            await check_and_notify_low_stock(message.bot, lang)

        else:
            await message.answer(get_text('cart_error', lang))

    except ValueError:
        await message.answer(get_text('invalid_price', lang))
        return

    await state.clear()


@inventory_router.callback_query(F.data.startswith("add_ml_variant_"))
@admin_only
async def start_add_ml_variant(callback: CallbackQuery, state: FSMContext):
    """
    ML variant qo'shish jarayonini boshlash
    """
    product_id = int(callback.data.split("_")[3])

    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    await state.update_data(product_id=product_id, lang=lang)
    await state.set_state(InventoryStates.waiting_for_ml_amount)

    await callback.message.edit_text(get_text('enter_ml_amount', lang))
    await callback.answer()


@inventory_router.message(InventoryStates.waiting_for_ml_amount)
@admin_only
async def process_ml_amount(message: Message, state: FSMContext):
    """
    ML miqdorini qabul qilish
    """
    data = await state.get_data()
    lang = data.get('lang', 'uz')

    try:
        ml_amount = int(message.text)

        if ml_amount <= 0:
            await message.answer("❌ ML miqdori 0 dan katta bo'lishi kerak")
            return

        await state.update_data(ml_amount=ml_amount)
        await state.set_state(InventoryStates.waiting_for_ml_price)

        await message.answer(get_text('enter_ml_price', lang))

    except ValueError:
        await message.answer(get_text('invalid_price', lang))


@inventory_router.message(InventoryStates.waiting_for_ml_price)
@admin_only
async def process_ml_price(message: Message, state: FSMContext):
    """
    ML variant narxini qabul qilish va qo'shish
    """
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    product_id = data.get('product_id')
    ml_amount = data.get('ml_amount')

    try:
        price = float(message.text)

        if price <= 0:
            await message.answer("❌ Narx 0 dan katta bo'lishi kerak")
            return

        result = await add_ml_variant(product_id, ml_amount, price)

        if result:
            await message.answer(get_text('ml_variant_added', lang))
        else:
            await message.answer("❌ ML variant allaqachon mavjud yoki xatolik yuz berdi")

    except ValueError:
        await message.answer(get_text('invalid_price', lang))
        return

    await state.clear()


@inventory_router.callback_query(F.data.startswith("delete_ml_"))
@admin_only
async def delete_ml_variant_handler(callback: CallbackQuery):
    """
    ML variantni o'chirish
    """
    variant_id = int(callback.data.split("_")[2])

    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    result = await delete_ml_variant(variant_id)

    if result:
        await callback.answer("✅ ML variant o'chirildi", show_alert=True)
    else:
        await callback.answer(get_text('delete_error', lang), show_alert=True)


@inventory_router.callback_query(F.data == "check_low_stock")
@admin_only
async def check_low_stock_handler(callback: CallbackQuery):
    """
    Kam qolgan mahsulotlarni ko'rsatish
    """
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    low_stock = await get_low_stock_products(lang)
    out_of_stock = await get_out_of_stock_products(lang)

    if not low_stock and not out_of_stock:
        await callback.answer(get_text('no_low_stock', lang), show_alert=True)
        return

    text = get_text('check_low_stock', lang) + "\n\n"

    if out_of_stock:
        text += "❌ Tugagan mahsulotlar:\n"
        for product in out_of_stock:
            text += f"  • {product['name']}\n"
        text += "\n"

    if low_stock:
        text += "⚠️ Kam qolgan mahsulotlar:\n"
        for product in low_stock:
            text += f"  • {product['name']} - {product['stock_quantity']} dona\n"

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=get_text('back', lang),
                callback_data="manage_inventory"
            )
        ]
    ])

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


async def check_and_notify_low_stock(bot, lang='uz'):
    """
    Kam qolgan mahsulotlarni tekshirish va adminlarga xabar berish
    """
    from database.db import get_admins

    low_stock = await get_low_stock_products(lang)
    out_of_stock = await get_out_of_stock_products(lang)

    if not low_stock and not out_of_stock:
        return

    products_text = ""

    if out_of_stock:
        products_text += "❌ Tugagan:\n"
        for product in out_of_stock:
            products_text += f"  • {product['name']}\n"
        products_text += "\n"

    if low_stock:
        products_text += "⚠️ Kam qolgan:\n"
        for product in low_stock:
            products_text += f"  • {product['name']} - {product['stock_quantity']} dona\n"

    text = get_text('low_stock_notification', lang).format(products=products_text)

    # Barcha adminlarga xabar yuborish
    admins = await get_admins()
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, text)
        except Exception as e:
            print(f"Failed to send low stock notification to admin {admin_id}: {e}")
