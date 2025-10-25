# handlers/user/product.py
"""
Mahsulot tanlash, ko'rish va savatga qo'shish handlerlari
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from database.db import get_user, get_product_by_id, add_to_cart
from keyboards.user_keyboards import (
    get_product_detail_keyboard,
    get_products_list_keyboard,
    get_back_to_category_keyboard
)
from utils.localization import get_text

product_router = Router()


@product_router.callback_query(F.data.startswith("product_"))
async def show_product_detail(callback: CallbackQuery):
    """
    Mahsulot tafsilotlarini ko'rsatish
    Format: product_<product_id>_<category>_<page>
    """
    data = callback.data.split("_")
    product_id = int(data[1])
    category = data[2]
    page = int(data[3])

    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    product = await get_product_by_id(product_id, lang)

    if not product:
        await callback.answer(get_text('product_not_found', lang), show_alert=True)
        return

    # Ombor miqdorini tekshirish
    from database.db import get_product_stock, check_product_availability
    stock = await get_product_stock(product_id)
    is_available = await check_product_availability(product_id, 1)

    # Mahsulot ma'lumotlarini tayyorlash
    product_text = get_text('product_detail', lang).format(
        name=product['name'],
        description=product['description'],
        price=f"{product['price']:,.0f}"
    )

    # Stock ma'lumotini qo'shish
    if stock is not None:
        if stock > 10:
            product_text += f"\n\n✅ {get_text('in_stock', lang)}"
        elif stock > 0:
            product_text += f"\n\n⚠️ {get_text('limited_stock', lang)}: {stock} ta"
        else:
            product_text += f"\n\n🚫 {get_text('out_of_stock', lang)}"

    # Caption uzunligini tekshirish (Telegram max 1024)
    max_caption_length = 1000
    if len(product_text) > max_caption_length:
        # Tavsifni qisqartirish
        short_description = product['description'][:200] + "..."
        product_text = get_text('product_detail', lang).format(
            name=product['name'],
            description=short_description,
            price=f"{product['price']:,.0f}"
        )
        if stock is not None:
            if stock > 10:
                product_text += f"\n\n✅ {get_text('in_stock', lang)}"
            elif stock > 0:
                product_text += f"\n\n⚠️ {get_text('limited_stock', lang)}: {stock} ta"
            else:
                product_text += f"\n\n🚫 {get_text('out_of_stock', lang)}"

    # Rasm bilan birga yuborish
    try:
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=product['image_url'],
            caption=product_text,
            reply_markup=get_product_detail_keyboard(product_id, category, page, lang, is_available)
        )
    except Exception as e:
        # Agar rasm yuborishda xatolik bo'lsa, faqat matnni yuboramiz
        await callback.message.edit_text(
            product_text,
            reply_markup=get_product_detail_keyboard(product_id, category, page, lang, is_available)
        )

    await callback.answer()


@product_router.callback_query(F.data.startswith("add_cart_"))
async def add_product_to_cart(callback: CallbackQuery):
    """
    Mahsulotni savatga qo'shish
    Format: add_cart_<product_id>
    """
    product_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id

    user = await get_user(user_id)
    lang = user.get('language', 'uz')

    # Savatga qo'shish
    result = await add_to_cart(user_id, product_id, quantity=1)

    if result:
        await callback.answer(
            get_text('added_to_cart', lang),
            show_alert=True
        )
    else:
        await callback.answer(
            get_text('cart_error', lang),
            show_alert=True
        )


@product_router.callback_query(F.data.startswith("back_category_"))
async def back_to_category_list(callback: CallbackQuery):
    """
    Kategoriya ro'yxatiga qaytish
    Format: back_category_<category>_<page>
    """
    from database.db import get_products_by_category

    data = callback.data.split("_")
    category = data[2]
    page = int(data[3])

    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    products = await get_products_by_category(category, lang)

    try:
        await callback.message.delete()
        await callback.message.answer(
            get_text('select_product', lang),
            reply_markup=get_products_list_keyboard(products, category, page, lang)
        )
    except:
        await callback.message.edit_text(
            get_text('select_product', lang),
            reply_markup=get_products_list_keyboard(products, category, page, lang)
        )

    await callback.answer()