# handlers/admin/add_product.py
"""
Admin uchun yangi mahsulot qo'shish (ConversationHandler)
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.db import get_user, create_product
from keyboards.admin_keyboards import (
    get_category_selection_keyboard,
    get_confirm_product_keyboard,
    get_admin_menu_keyboard
)
from utils.decorators import admin_only
from utils.localization import get_text
from utils.validators import validate_price, validate_image

add_product_router = Router()


# FSM uchun holatlar
class AddProductStates(StatesGroup):
    waiting_for_name_uz = State()
    waiting_for_name_ru = State()
    waiting_for_description_uz = State()
    waiting_for_description_ru = State()
    waiting_for_price = State()
    waiting_for_category = State()
    waiting_for_image = State()
    waiting_for_confirm = State()


@add_product_router.callback_query(F.data == "admin_add_product")
@admin_only
async def start_add_product(callback: CallbackQuery, state: FSMContext):
    """
    Yangi mahsulot qo'shish jarayonini boshlash
    """
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    await callback.message.edit_text(
        get_text('enter_product_name_uz', lang),
        reply_markup=None
    )

    await state.set_state(AddProductStates.waiting_for_name_uz)
    await callback.answer()


@add_product_router.message(AddProductStates.waiting_for_name_uz, F.text)
@admin_only
async def process_name_uz(message: Message, state: FSMContext):
    """
    O'zbekcha nom qabul qilish
    """
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'uz')

    name_uz = message.text.strip()

    if len(name_uz) < 3:
        await message.answer(get_text('name_too_short', lang))
        return

    await state.update_data(name_uz=name_uz)

    await message.answer(get_text('enter_product_name_ru', lang))
    await state.set_state(AddProductStates.waiting_for_name_ru)


@add_product_router.message(AddProductStates.waiting_for_name_ru, F.text)
@admin_only
async def process_name_ru(message: Message, state: FSMContext):
    """
    Ruscha nom qabul qilish
    """
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'uz')

    name_ru = message.text.strip()

    if len(name_ru) < 3:
        await message.answer(get_text('name_too_short', lang))
        return

    await state.update_data(name_ru=name_ru)

    await message.answer(get_text('enter_description_uz', lang))
    await state.set_state(AddProductStates.waiting_for_description_uz)


@add_product_router.message(AddProductStates.waiting_for_description_uz, F.text)
@admin_only
async def process_description_uz(message: Message, state: FSMContext):
    """
    O'zbekcha tavsif qabul qilish
    """
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'uz')

    description_uz = message.text.strip()

    if len(description_uz) < 10:
        await message.answer(get_text('description_too_short', lang))
        return

    if len(description_uz) > 500:
        await message.answer(
            "❌ Tavsif juda uzun. Maksimal 500 belgi.\n"
            f"Sizning tavsif: {len(description_uz)} belgi"
        )
        return

    await state.update_data(description_uz=description_uz)

    await message.answer(get_text('enter_description_ru', lang))
    await state.set_state(AddProductStates.waiting_for_description_ru)


@add_product_router.message(AddProductStates.waiting_for_description_ru, F.text)
@admin_only
async def process_description_ru(message: Message, state: FSMContext):
    """
    Ruscha tavsif qabul qilish
    """
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'uz')

    description_ru = message.text.strip()

    if len(description_ru) < 10:
        await message.answer(get_text('description_too_short', lang))
        return

    if len(description_ru) > 500:
        await message.answer(
            "❌ Описание слишком длинное. Максимум 500 символов.\n"
            f"Ваше описание: {len(description_ru)} символов"
        )
        return

    await state.update_data(description_ru=description_ru)

    await message.answer(get_text('enter_price', lang))
    await state.set_state(AddProductStates.waiting_for_price)


@add_product_router.message(AddProductStates.waiting_for_price, F.text)
@admin_only
async def process_price(message: Message, state: FSMContext):
    """
    Narxni qabul qilish va tekshirish
    """
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'uz')

    price_text = message.text.strip()

    # Narxni tekshirish
    price = validate_price(price_text)

    if price is None:
        await message.answer(get_text('invalid_price', lang))
        return

    await state.update_data(price=price)

    await message.answer(
        get_text('select_category', lang),
        reply_markup=get_category_selection_keyboard(lang)
    )

    await state.set_state(AddProductStates.waiting_for_category)


@add_product_router.callback_query(AddProductStates.waiting_for_category, F.data.startswith("category_"))
@admin_only
async def process_category(callback: CallbackQuery, state: FSMContext):
    """
    Kategoriyani tanlash
    """
    category = callback.data.split("_")[1]  # category_men, category_women, category_unisex
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    await state.update_data(category=category)

    await callback.message.edit_text(
        get_text('send_product_image', lang),
        reply_markup=None
    )

    await state.set_state(AddProductStates.waiting_for_image)
    await callback.answer()


@add_product_router.message(AddProductStates.waiting_for_image, F.photo)
@admin_only
async def process_image(message: Message, state: FSMContext):
    """
    Mahsulot rasmini qabul qilish
    """
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'uz')

    # Eng katta o'lchamli rasmni olish
    photo = message.photo[-1]
    file_id = photo.file_id

    await state.update_data(image_url=file_id)

    # Mahsulot ma'lumotlarini ko'rsatish va tasdiqlash
    data = await state.get_data()

    # Qisqa caption (1024 belgi limit)
    caption_text = get_text('product_preview', lang) + "\n\n"
    caption_text += f"🇺🇿 {data['name_uz']}\n"
    caption_text += f"🇷🇺 {data['name_ru']}\n\n"
    caption_text += f"💰 {data['price']:,.0f} so'm | 📂 {data['category'].upper()}"

    # Tafsilotli ma'lumot alohida xabar sifatida
    detail_text = f"📝 {get_text('enter_description_uz', lang)}\n{data['description_uz']}\n\n"
    detail_text += f"📝 {get_text('enter_description_ru', lang)}\n{data['description_ru']}"

    # Agar tavsif juda uzun bo'lsa, qisqartirish
    max_caption_length = 900  # 1024 dan past, xavfsizlik uchun
    if len(caption_text + "\n\n" + detail_text) > max_caption_length:
        # Faqat qisqa ma'lumot bilan rasm yuborish
        await message.answer_photo(
            photo=file_id,
            caption=caption_text,
            reply_markup=get_confirm_product_keyboard(lang)
        )
        # Tavsifni alohida yuborish
        await message.answer(detail_text)
    else:
        # Hammasi bir xabarda
        full_caption = caption_text + "\n\n" + detail_text
        await message.answer_photo(
            photo=file_id,
            caption=full_caption,
            reply_markup=get_confirm_product_keyboard(lang)
        )

    await state.set_state(AddProductStates.waiting_for_confirm)


@add_product_router.callback_query(AddProductStates.waiting_for_confirm, F.data == "confirm_product")
@admin_only
async def confirm_product(callback: CallbackQuery, state: FSMContext):
    """
    Mahsulotni tasdiqlash va bazaga saqlash
    """
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    data = await state.get_data()

    # Mahsulotni bazaga saqlash
    product = await create_product(
        name_uz=data['name_uz'],
        name_ru=data['name_ru'],
        description_uz=data['description_uz'],
        description_ru=data['description_ru'],
        price=data['price'],
        category=data['category'],
        image_url=data['image_url']
    )

    if product:
        await callback.message.edit_caption(
            caption=get_text('product_added', lang),
            reply_markup=None
        )

        await callback.message.answer(
            get_text('admin_welcome', lang),
            reply_markup=get_admin_menu_keyboard(lang)
        )

        await state.clear()
    else:
        await callback.answer(get_text('product_add_error', lang), show_alert=True)

    await callback.answer()


@add_product_router.callback_query(AddProductStates.waiting_for_confirm, F.data == "cancel_product")
@admin_only
async def cancel_product(callback: CallbackQuery, state: FSMContext):
    """
    Mahsulot qo'shishni bekor qilish
    """
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    await callback.message.edit_caption(
        caption=get_text('product_cancelled', lang),
        reply_markup=None
    )

    await callback.message.answer(
        get_text('admin_welcome', lang),
        reply_markup=get_admin_menu_keyboard(lang)
    )

    await state.clear()
    await callback.answer()


@add_product_router.message(AddProductStates.waiting_for_image)
@admin_only
async def invalid_image(message: Message):
    """
    Noto'g'ri fayl yuborilganda
    """
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'uz')

    await message.answer(get_text('invalid_image', lang))