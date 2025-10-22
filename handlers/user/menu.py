# handlers/user/menu.py
"""
Asosiy menyu handlerlari: kategoriyalar, sozlamalar, biz haqimizda
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.db import get_user, get_products_by_category
from keyboards.user_keyboards import (
    get_main_menu_keyboard,
    get_categories_keyboard,
    get_products_list_keyboard,
    get_settings_keyboard,
    get_back_to_main_menu_keyboard
)
from utils.localization import get_text

menu_router = Router()


@menu_router.message(F.text.in_(['👨 Erkaklar atirlari', '👨 Мужские духи']))
async def show_men_category(message: Message):
    """
    Erkaklar atirlari kategoriyasini ko'rsatish
    """
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'uz')

    products = await get_products_by_category('men', lang)

    if not products:
        await message.answer(
            get_text('no_products', lang),
            reply_markup=get_back_to_main_menu_keyboard(lang)
        )
        return

    await message.answer(
        get_text('select_product', lang),
        reply_markup=get_products_list_keyboard(products, 'men', 0, lang)
    )


@menu_router.message(F.text.in_(['👩 Ayollar atirlari', '👩 Женские духи']))
async def show_women_category(message: Message):
    """
    Ayollar atirlari kategoriyasini ko'rsatish
    """
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'uz')

    products = await get_products_by_category('women', lang)

    if not products:
        await message.answer(
            get_text('no_products', lang),
            reply_markup=get_back_to_main_menu_keyboard(lang)
        )
        return

    await message.answer(
        get_text('select_product', lang),
        reply_markup=get_products_list_keyboard(products, 'women', 0, lang)
    )


@menu_router.message(F.text.in_(['👥 Uniseks atirlar', '👥 Унисекс духи']))
async def show_unisex_category(message: Message):
    """
    Uniseks atirlar kategoriyasini ko'rsatish
    """
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'uz')

    products = await get_products_by_category('unisex', lang)

    if not products:
        await message.answer(
            get_text('no_products', lang),
            reply_markup=get_back_to_main_menu_keyboard(lang)
        )
        return

    await message.answer(
        get_text('select_product', lang),
        reply_markup=get_products_list_keyboard(products, 'unisex', 0, lang)
    )


@menu_router.message(F.text.in_(['ℹ️ Biz haqimizda', 'ℹ️ О нас']))
async def show_about_us(message: Message):
    """
    Biz haqimizda ma'lumot
    """
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'uz')

    about_text = get_text('about_us', lang)
    contact_text = get_text('contact_info', lang)

    await message.answer(
        f"{about_text}\n\n{contact_text}",
        reply_markup=get_back_to_main_menu_keyboard(lang)
    )


@menu_router.message(F.text.in_(['⚙️ Sozlamalar', '⚙️ Настройки']))
async def show_settings(message: Message):
    """
    Sozlamalar menyusi
    """
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'uz')

    await message.answer(
        get_text('settings_menu', lang),
        reply_markup=get_settings_keyboard(lang)
    )


@menu_router.callback_query(F.data == "back_to_main")
async def back_to_main_menu(callback: CallbackQuery):
    """
    Asosiy menyuga qaytish
    """
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    await callback.message.edit_text(
        get_text('main_menu', lang),
        reply_markup=get_main_menu_keyboard(lang)
    )
    await callback.answer()


@menu_router.callback_query(F.data.startswith("page_"))
async def pagination_handler(callback: CallbackQuery):
    """
    Mahsulotlar ro'yxatida sahifalash (pagination)
    Format: page_<category>_<page_num>
    """
    data = callback.data.split("_")
    category = data[1]
    page = int(data[2])

    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    products = await get_products_by_category(category, lang)

    await callback.message.edit_text(
        get_text('select_product', lang),
        reply_markup=get_products_list_keyboard(products, category, page, lang)
    )
    await callback.answer()