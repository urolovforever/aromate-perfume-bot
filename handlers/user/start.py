# handlers/user/start.py
"""
/start komandasi va til tanlash handleri
"""

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.db import get_user, create_user, update_user_language
from keyboards.user_keyboards import get_language_keyboard, get_main_menu_keyboard
from utils.localization import get_text

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """
    /start komandasi - foydalanuvchini saqlab, til tanlashni taklif qilish
    """
    user_id = message.from_user.id
    user = await get_user(user_id)

    if not user:
        # Yangi foydalanuvchi - bazaga qo'shamiz (default: uz)
        await create_user(
            user_id=user_id,
            username=message.from_user.username or "unknown",
            full_name=message.from_user.full_name or "User",
            language="uz"
        )

        # Til tanlash menyusini ko'rsatamiz
        await message.answer(
            "🇺🇿 Tilni tanlang / 🇷🇺 Выберите язык:",
            reply_markup=get_language_keyboard()
        )
    else:
        # Mavjud foydalanuvchi - asosiy menyuni ko'rsatamiz
        lang = user.get('language', 'uz')
        welcome_text = get_text('welcome', lang).format(
            name=message.from_user.full_name
        )

        await message.answer(
            welcome_text,
            reply_markup=get_main_menu_keyboard(lang)
        )


@start_router.callback_query(F.data.startswith("lang_"))
async def select_language(callback: CallbackQuery, state: FSMContext):
    """
    Til tanlash callback handleri
    """
    lang = callback.data.split("_")[1]  # lang_uz yoki lang_ru
    user_id = callback.from_user.id

    # Foydalanuvchi tilini yangilash
    await update_user_language(user_id, lang)

    # Til tanlandi xabarini ko'rsatish
    await callback.message.edit_text(
        get_text('language_selected', lang),
        reply_markup=None
    )

    # Asosiy menyuni ko'rsatish
    welcome_text = get_text('welcome', lang).format(
        name=callback.from_user.full_name
    )

    await callback.message.answer(
        welcome_text,
        reply_markup=get_main_menu_keyboard(lang)
    )

    await callback.answer()


@start_router.callback_query(F.data == "change_language")
async def change_language_handler(callback: CallbackQuery):
    """
    Tilni o'zgartirish uchun handler (sozlamalardan)
    """
    await callback.message.edit_text(
        "🇺🇿 Tilni tanlang / 🇷🇺 Выберите язык:",
        reply_markup=get_language_keyboard()
    )
    await callback.answer()