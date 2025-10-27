# handlers/admin/inventory.py
"""
Admin ombor boshqaruvi handlerlari - yangilangan qulay versiya
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
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

    text = "📦 " + get_text('manage_inventory', lang) + "\n\n"
    text += "Mahsulotni tanlang va boshqaring:" if lang == 'uz' else "Выберите товар для управления:"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📋 " + get_text('admin_products_list', lang),
                callback_data="inventory_products_list"
            )
        ],
        [
            InlineKeyboardButton(
                text="⚠️ " + get_text('check_low_stock', lang),
                callback_data="check_low_stock"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ " + get_text('back', lang),
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

    text = "📦 " + get_text('products_list_title', lang) + "\n\n"
    text += "Mahsulotni bosing:" if lang == 'uz' else "Нажмите на товар:"

    buttons = []
    for product in products:
        # Stock holati emoji
        if product['stock_quantity'] == 0:
            stock_emoji = "❌"
            stock_text = "Tugagan" if lang == 'uz' else "Нет"
        elif product['stock_quantity'] <= product.get('low_stock_threshold', 5):
            stock_emoji = "⚠️"
            stock_text = f"{product['stock_quantity']} dona"
        else:
            stock_emoji = "✅"
            stock_text = f"{product['stock_quantity']} dona"

        button_text = f"{stock_emoji} {product['name_uz'][:25]} • {stock_text}"
        buttons.append([
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"inv_prod_{product['id']}"
            )
        ])

    # Orqaga qaytish
    buttons.append([
        InlineKeyboardButton(
            text="⬅️ " + get_text('back', lang),
            callback_data="manage_inventory"
        )
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@inventory_router.callback_query(F.data.startswith("inv_prod_"))
@admin_only
async def show_product_inventory(callback: CallbackQuery):
    """
    Mahsulot ombor ma'lumotlarini ko'rsatish va boshqarish
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

    # Mahsulot kartasi
    text = f"🎁 <b>{product['name']}</b>\n\n"

    # Ombor holati
    stock_qty = product['stock_quantity']
    if stock_qty == 0:
        text += f"📦 Ombor: ❌ <b>Tugagan</b>\n"
    elif stock_qty <= product.get('low_stock_threshold', 5):
        text += f"📦 Ombor: ⚠️ <b>{stock_qty} dona</b> (Kam qoldi!)\n"
    else:
        text += f"📦 Ombor: ✅ <b>{stock_qty} dona</b>\n"

    text += f"💰 Narx: <b>{product['price']:,.0f}</b> {get_text('sum', lang)}\n"
    text += f"📂 Kategoriya: {product['category']}\n"

    # ML variantlar
    if ml_variants:
        text += f"\n💧 <b>ML Variantlar:</b>\n"
        for variant in ml_variants:
            text += f"  • {variant['ml_amount']} ML - {variant['price']:,.0f} {get_text('sum', lang)}\n"
    else:
        text += f"\n💧 ML variantlar: <i>Yo'q</i>\n"

    # Keyboard
    buttons = [
        [
            InlineKeyboardButton(
                text="➕ Tez qo'shish (+10)",
                callback_data=f"quick_add_{product_id}_10"
            ),
            InlineKeyboardButton(
                text="➕ Tez qo'shish (+50)",
                callback_data=f"quick_add_{product_id}_50"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Qo'lda miqdor kiritish",
                callback_data=f"manual_stock_{product_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="💧 ML variant qo'shish",
                callback_data=f"add_ml_menu_{product_id}"
            )
        ]
    ]

    # ML variantlarni boshqarish
    if ml_variants:
        buttons.append([
            InlineKeyboardButton(
                text="🗑 ML variantlarni boshqarish",
                callback_data=f"manage_ml_{product_id}"
            )
        ])

    # Orqaga
    buttons.append([
        InlineKeyboardButton(
            text="⬅️ Orqaga",
            callback_data="inventory_products_list"
        )
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@inventory_router.callback_query(F.data.startswith("quick_add_"))
@admin_only
async def quick_add_stock(callback: CallbackQuery):
    """
    Tez miqdor qo'shish (+10, +50)
    """
    data = callback.data.split("_")
    product_id = int(data[2])
    amount = int(data[3])

    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    # Hozirgi miqdorni olish
    product = await get_product_by_id(product_id, lang)
    if not product:
        await callback.answer(get_text('product_not_found', lang), show_alert=True)
        return

    new_stock = product['stock_quantity'] + amount

    # Yangilash
    result = await update_product_stock(product_id, new_stock)

    if result:
        await callback.answer(f"✅ +{amount} dona qo'shildi! Jami: {new_stock}", show_alert=True)

        # Sahifani yangilash
        await show_product_inventory(callback)

        # Kam qolgan mahsulotlarni tekshirish
        await check_and_notify_low_stock(callback.bot, lang)
    else:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@inventory_router.callback_query(F.data.startswith("manual_stock_"))
@admin_only
async def start_manual_stock(callback: CallbackQuery, state: FSMContext):
    """
    Qo'lda miqdor kiritish
    """
    product_id = int(callback.data.split("_")[2])

    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    product = await get_product_by_id(product_id, lang)

    text = f"📦 <b>{product['name']}</b>\n\n"
    text += f"Hozirgi miqdor: <b>{product['stock_quantity']} dona</b>\n\n"
    text += "Yangi miqdorni kiriting:\n" if lang == 'uz' else "Введите новое количество:\n"
    text += "<i>Masalan: 100</i>" if lang == 'uz' else "<i>Например: 100</i>"

    await state.update_data(product_id=product_id, lang=lang)
    await state.set_state(InventoryStates.waiting_for_stock)

    # Bekor qilish tugmasi
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
                callback_data=f"cancel_stock_{product_id}"
            )
        ]
    ])

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@inventory_router.message(InventoryStates.waiting_for_stock)
@admin_only
async def process_manual_stock(message: Message, state: FSMContext):
    """
    Qo'lda kiritilgan miqdorni qabul qilish
    """
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    product_id = data.get('product_id')

    try:
        new_stock = int(message.text.strip())

        if new_stock < 0:
            await message.answer("❌ Miqdor 0 dan katta bo'lishi kerak!" if lang == 'uz' else "❌ Количество должно быть больше 0!")
            return

        result = await update_product_stock(product_id, new_stock)

        if result:
            await message.answer(
                f"✅ Yangilandi! Yangi miqdor: <b>{new_stock} dona</b>",
                parse_mode="HTML"
            )

            # Kam qolgan mahsulotlarni tekshirish
            await check_and_notify_low_stock(message.bot, lang)
        else:
            await message.answer("❌ Xatolik yuz berdi" if lang == 'uz' else "❌ Произошла ошибка")

    except ValueError:
        await message.answer("❌ Faqat raqam kiriting!" if lang == 'uz' else "❌ Введите только число!")
        return

    await state.clear()


@inventory_router.callback_query(F.data.startswith("cancel_stock_"))
async def cancel_stock_input(callback: CallbackQuery, state: FSMContext):
    """
    Miqdor kiritishni bekor qilish
    """
    product_id = int(callback.data.split("_")[2])
    await state.clear()

    # Mahsulot kartasiga qaytish
    callback.data = f"inv_prod_{product_id}"
    await show_product_inventory(callback)


@inventory_router.callback_query(F.data.startswith("add_ml_menu_"))
@admin_only
async def show_ml_variant_menu(callback: CallbackQuery):
    """
    ML variant qo'shish menyusi (tez tanlovlar)
    """
    product_id = int(callback.data.split("_")[3])

    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    product = await get_product_by_id(product_id, lang)

    text = f"💧 <b>ML variant qo'shish</b>\n\n"
    text += f"Mahsulot: {product['name']}\n\n"
    text += "Tez tanlov yoki qo'lda kiriting:" if lang == 'uz' else "Быстрый выбор или введите вручную:"

    # Preset ML miqdorlari
    buttons = [
        [
            InlineKeyboardButton(text="5 ML", callback_data=f"quick_ml_{product_id}_5"),
            InlineKeyboardButton(text="10 ML", callback_data=f"quick_ml_{product_id}_10"),
            InlineKeyboardButton(text="15 ML", callback_data=f"quick_ml_{product_id}_15")
        ],
        [
            InlineKeyboardButton(text="20 ML", callback_data=f"quick_ml_{product_id}_20"),
            InlineKeyboardButton(text="30 ML", callback_data=f"quick_ml_{product_id}_30"),
            InlineKeyboardButton(text="50 ML", callback_data=f"quick_ml_{product_id}_50")
        ],
        [
            InlineKeyboardButton(
                text="✏️ Qo'lda kiriting" if lang == 'uz' else "✏️ Ввести вручную",
                callback_data=f"manual_ml_{product_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Orqaga",
                callback_data=f"inv_prod_{product_id}"
            )
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@inventory_router.callback_query(F.data.startswith("quick_ml_"))
@admin_only
async def quick_add_ml_variant(callback: CallbackQuery, state: FSMContext):
    """
    Tez ML variant qo'shish (faqat narxni so'rash)
    """
    data = callback.data.split("_")
    product_id = int(data[2])
    ml_amount = int(data[3])

    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    product = await get_product_by_id(product_id, lang)

    text = f"💧 <b>{ml_amount} ML variant</b>\n\n"
    text += f"Mahsulot: {product['name']}\n"
    text += f"Miqdor: <b>{ml_amount} ML</b>\n\n"
    text += "Narxni kiriting (so'mda):\n" if lang == 'uz' else "Введите цену (в сумах):\n"
    text += f"<i>Masalan: {int(product['price'] * ml_amount / 100):,.0f}</i>"

    await state.update_data(product_id=product_id, ml_amount=ml_amount, lang=lang)
    await state.set_state(InventoryStates.waiting_for_ml_price)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data=f"cancel_ml_{product_id}"
            )
        ]
    ])

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@inventory_router.callback_query(F.data.startswith("manual_ml_"))
@admin_only
async def start_manual_ml(callback: CallbackQuery, state: FSMContext):
    """
    Qo'lda ML variant qo'shish
    """
    product_id = int(callback.data.split("_")[2])

    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    product = await get_product_by_id(product_id, lang)

    text = f"💧 <b>ML variant qo'shish</b>\n\n"
    text += f"Mahsulot: {product['name']}\n\n"
    text += "ML miqdorini kiriting:\n" if lang == 'uz' else "Введите количество ML:\n"
    text += "<i>Masalan: 25</i>"

    await state.update_data(product_id=product_id, lang=lang)
    await state.set_state(InventoryStates.waiting_for_ml_amount)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data=f"cancel_ml_{product_id}"
            )
        ]
    ])

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
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
        ml_amount = int(message.text.strip())

        if ml_amount <= 0:
            await message.answer("❌ ML miqdori 0 dan katta bo'lishi kerak!")
            return

        await state.update_data(ml_amount=ml_amount)
        await state.set_state(InventoryStates.waiting_for_ml_price)

        await message.answer(
            f"✅ {ml_amount} ML\n\n"
            f"Endi narxni kiriting (so'mda):\n"
            f"<i>Masalan: 50000</i>",
            parse_mode="HTML"
        )

    except ValueError:
        await message.answer("❌ Faqat raqam kiriting!")


@inventory_router.message(InventoryStates.waiting_for_ml_price)
@admin_only
async def process_ml_price(message: Message, state: FSMContext):
    """
    ML variant narxini qabul qilish va saqlash
    """
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    product_id = data.get('product_id')
    ml_amount = data.get('ml_amount')

    try:
        price = float(message.text.strip().replace(',', '').replace(' ', ''))

        if price <= 0:
            await message.answer("❌ Narx 0 dan katta bo'lishi kerak!")
            return

        result = await add_ml_variant(product_id, ml_amount, price)

        if result:
            await message.answer(
                f"✅ <b>ML variant qo'shildi!</b>\n\n"
                f"💧 {ml_amount} ML - {price:,.0f} so'm",
                parse_mode="HTML"
            )
        else:
            await message.answer(
                "❌ Xatolik! Bu variant allaqachon mavjud yoki xatolik yuz berdi."
            )

    except ValueError:
        await message.answer("❌ Noto'g'ri narx! Faqat raqam kiriting.")
        return

    await state.clear()


@inventory_router.callback_query(F.data.startswith("cancel_ml_"))
async def cancel_ml_input(callback: CallbackQuery, state: FSMContext):
    """
    ML qo'shishni bekor qilish
    """
    product_id = int(callback.data.split("_")[2])
    await state.clear()

    # Mahsulot kartasiga qaytish
    callback.data = f"inv_prod_{product_id}"
    await show_product_inventory(callback)


@inventory_router.callback_query(F.data.startswith("manage_ml_"))
@admin_only
async def manage_ml_variants(callback: CallbackQuery):
    """
    ML variantlarni boshqarish (o'chirish)
    """
    product_id = int(callback.data.split("_")[2])

    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    product = await get_product_by_id(product_id, lang)
    ml_variants = await get_ml_variants(product_id)

    text = f"🗑 <b>ML variantlarni boshqarish</b>\n\n"
    text += f"Mahsulot: {product['name']}\n\n"
    text += "O'chirish uchun bosing:"

    buttons = []
    for variant in ml_variants:
        buttons.append([
            InlineKeyboardButton(
                text=f"🗑 {variant['ml_amount']} ML - {variant['price']:,.0f} so'm",
                callback_data=f"del_ml_{variant['id']}_{product_id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="⬅️ Orqaga",
            callback_data=f"inv_prod_{product_id}"
        )
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@inventory_router.callback_query(F.data.startswith("del_ml_"))
@admin_only
async def delete_ml_variant_handler(callback: CallbackQuery):
    """
    ML variantni o'chirish
    """
    data = callback.data.split("_")
    variant_id = int(data[2])
    product_id = int(data[3])

    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    result = await delete_ml_variant(variant_id)

    if result:
        await callback.answer("✅ ML variant o'chirildi", show_alert=True)

        # Boshqaruv sahifasiga qaytish
        callback.data = f"manage_ml_{product_id}"
        await manage_ml_variants(callback)
    else:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


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

    text = "⚠️ <b>Ombor ogohlantirishi</b>\n\n"

    if out_of_stock:
        text += "❌ <b>Tugagan mahsulotlar:</b>\n"
        for product in out_of_stock:
            text += f"  • {product['name']}\n"
        text += "\n"

    if low_stock:
        text += "⚠️ <b>Kam qolgan mahsulotlar:</b>\n"
        for product in low_stock:
            text += f"  • {product['name']} - <b>{product['stock_quantity']} dona</b>\n"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⬅️ Orqaga",
                callback_data="manage_inventory"
            )
        ]
    ])

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
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
        products_text += "❌ <b>Tugagan:</b>\n"
        for product in out_of_stock:
            products_text += f"  • {product['name']}\n"
        products_text += "\n"

    if low_stock:
        products_text += "⚠️ <b>Kam qolgan:</b>\n"
        for product in low_stock:
            products_text += f"  • {product['name']} - {product['stock_quantity']} dona\n"

    text = "⚠️ <b>OMBOR OGOHLANTIRISHI!</b>\n\n"
    text += "Quyidagi mahsulotlar tugab qolmoqda:\n\n" if lang == 'uz' else "Следующие товары заканчиваются:\n\n"
    text += products_text

    # Barcha adminlarga xabar yuborish
    admins = await get_admins()
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, text, parse_mode="HTML")
        except Exception as e:
            print(f"Failed to send low stock notification to admin {admin_id}: {e}")
