# keyboards/user_keyboards.py
"""
Foydalanuvchilar uchun klaviaturalar
"""

from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from typing import List, Dict
from utils.localization import get_text


def get_language_keyboard() -> InlineKeyboardMarkup:
    """
    Til tanlash klaviaturasi
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")
        ]
    ])
    return keyboard


def get_main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """
    Asosiy menyu klaviaturasi
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_text('menu_men', lang)),
                KeyboardButton(text=get_text('menu_women', lang))
            ],
            [
                KeyboardButton(text=get_text('menu_unisex', lang)),
                KeyboardButton(text=get_text('menu_cart', lang))
            ],
            [
                KeyboardButton(text=get_text('menu_about', lang)),
                KeyboardButton(text=get_text('menu_settings', lang))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_products_list_keyboard(products: List[Dict], category: str,
                               page: int, lang: str) -> InlineKeyboardMarkup:
    """
    Mahsulotlar ro'yxati klaviaturasi (pagination bilan)
    """
    ITEMS_PER_PAGE = 5
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE

    buttons = []

    # Mahsulotlar tugmalari
    for product in products[start_idx:end_idx]:
        buttons.append([
            InlineKeyboardButton(
                text=f"{product['name']} - {product['price']:,.0f} {get_text('sum', lang)}",
                callback_data=f"product_{product['id']}_{category}_{page}"
            )
        ])

    # Pagination tugmalari
    nav_buttons = []

    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(text="◀️ " + get_text('previous', lang),
                                 callback_data=f"page_{category}_{page - 1}")
        )

    if end_idx < len(products):
        nav_buttons.append(
            InlineKeyboardButton(text=get_text('next', lang) + " ▶️",
                                 callback_data=f"page_{category}_{page + 1}")
        )

    if nav_buttons:
        buttons.append(nav_buttons)

    # Asosiy menyuga qaytish
    buttons.append([
        InlineKeyboardButton(text=get_text('back_to_menu', lang),
                             callback_data="back_to_main")
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_product_detail_keyboard(product_id: int, category: str,
                                page: int, lang: str) -> InlineKeyboardMarkup:
    """
    Mahsulot tafsilotlari klaviaturasi
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('add_to_cart', lang),
                                 callback_data=f"add_cart_{product_id}")
        ],
        [
            InlineKeyboardButton(text=get_text('back', lang),
                                 callback_data=f"back_category_{category}_{page}")
        ]
    ])
    return keyboard


def get_back_to_category_keyboard(category: str, page: int, lang: str) -> InlineKeyboardMarkup:
    """
    Kategoriyaga qaytish klaviaturasi
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('back', lang),
                                 callback_data=f"back_category_{category}_{page}")
        ]
    ])
    return keyboard


def get_cart_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Savat klaviaturasi (umumiy amallar)
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('checkout', lang),
                                 callback_data="checkout")
        ],
        [
            InlineKeyboardButton(text=get_text('clear_cart', lang),
                                 callback_data="clear_cart")
        ],
        [
            InlineKeyboardButton(text=get_text('back_to_menu', lang),
                                 callback_data="back_to_main")
        ]
    ])
    return keyboard


def get_checkout_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Buyurtma berish klaviaturasi
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('checkout', lang),
                                 callback_data="checkout")
        ],
        [
            InlineKeyboardButton(text=get_text('cancel', lang),
                                 callback_data="back_to_main")
        ]
    ])
    return keyboard


def get_phone_request_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """
    Telefon raqami so'rash klaviaturasi
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_text('send_contact', lang),
                               request_contact=True)
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def get_payment_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    To'lov turini tanlash klaviaturasi
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('payment_cash', lang),
                                 callback_data="payment_cash")
        ],
        [
            InlineKeyboardButton(text="💳 Click",
                                 callback_data="payment_click")
        ],
        [
            InlineKeyboardButton(text="💳 Payme",
                                 callback_data="payment_payme")
        ]
    ])
    return keyboard


def get_settings_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Sozlamalar klaviaturasi
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('change_language', lang),
                                 callback_data="change_language")
        ],
        [
            InlineKeyboardButton(text=get_text('back_to_menu', lang),
                                 callback_data="back_to_main")
        ]
    ])
    return keyboard


def get_back_to_main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Asosiy menyuga qaytish klaviaturasi
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('back_to_menu', lang),
                                 callback_data="back_to_main")
        ]
    ])
    return keyboard


def get_categories_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """
    Kategoriyalar klaviaturasi
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_text('menu_men', lang)),
                KeyboardButton(text=get_text('menu_women', lang))
            ],
            [
                KeyboardButton(text=get_text('menu_unisex', lang))
            ],
            [
                KeyboardButton(text=get_text('back_to_menu', lang))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard