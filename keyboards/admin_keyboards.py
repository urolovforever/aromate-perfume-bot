# keyboards/admin_keyboards.py
"""
Admin uchun klaviaturalar
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict
from utils.localization import get_text


def get_admin_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Admin asosiy menyu klaviaturasi
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('admin_add_product', lang),
                                 callback_data="admin_add_product")
        ],
        [
            InlineKeyboardButton(text=get_text('admin_products_list', lang),
                                 callback_data="admin_products_list")
        ],
        [
            InlineKeyboardButton(text=get_text('admin_orders_list', lang),
                                 callback_data="admin_orders_list")
        ],
        [
            InlineKeyboardButton(text=get_text('admin_statistics', lang),
                                 callback_data="admin_statistics")
        ]
    ])
    return keyboard


def get_category_selection_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Kategoriya tanlash klaviaturasi (mahsulot qo'shishda)
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('category_men', lang),
                                 callback_data="category_men")
        ],
        [
            InlineKeyboardButton(text=get_text('category_women', lang),
                                 callback_data="category_women")
        ],
        [
            InlineKeyboardButton(text=get_text('category_unisex', lang),
                                 callback_data="category_unisex")
        ]
    ])
    return keyboard


def get_confirm_product_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Mahsulotni tasdiqlash klaviaturasi
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('confirm', lang),
                                 callback_data="confirm_product"),
            InlineKeyboardButton(text=get_text('cancel', lang),
                                 callback_data="cancel_product")
        ]
    ])
    return keyboard


def get_products_admin_keyboard(products: List[Dict], page: int,
                                lang: str) -> InlineKeyboardMarkup:
    """
    Admin uchun mahsulotlar ro'yxati klaviaturasi
    """
    ITEMS_PER_PAGE = 5
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE

    buttons = []

    # Mahsulotlar tugmalari
    for product in products[start_idx:end_idx]:
        buttons.append([
            InlineKeyboardButton(
                text=f"🗑 {product['name_uz'][:30]}...",
                callback_data=f"delete_product_{product['id']}"
            )
        ])

    # Pagination tugmalari
    nav_buttons = []

    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(text="◀️ " + get_text('previous', lang),
                                 callback_data=f"admin_page_{page - 1}")
        )

    if end_idx < len(products):
        nav_buttons.append(
            InlineKeyboardButton(text=get_text('next', lang) + " ▶️",
                                 callback_data=f"admin_page_{page + 1}")
        )

    if nav_buttons:
        buttons.append(nav_buttons)

    # Admin menyuga qaytish
    buttons.append([
        InlineKeyboardButton(text=get_text('back', lang),
                             callback_data="back_to_admin")
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_orders_keyboard(orders: List[Dict], page: int, lang: str, filter_type: str = 'all') -> InlineKeyboardMarkup:
    """
    Buyurtmalar ro'yxati klaviaturasi
    """
    ITEMS_PER_PAGE = 10
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE

    buttons = []

    # Buyurtmalar tugmalari
    for order in orders[start_idx:end_idx]:
        status_emoji = {
            'new': '🆕',
            'processing': '⏳',
            'delivering': '🚚',
            'completed': '✅',
            'cancelled': '❌'
        }

        emoji = status_emoji.get(order['status'], '📦')
        buttons.append([
            InlineKeyboardButton(
                text=f"{emoji} #{order['id']} - {order['user_name'][:15]} - {order['total']:,.0f}",
                callback_data=f"order_detail_{order['id']}"
            )
        ])

    # Pagination tugmalari
    nav_buttons = []

    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(text="◀️ " + get_text('previous', lang),
                                 callback_data=f"orders_filter_{filter_type}_{page - 1}")
        )

    if end_idx < len(orders):
        nav_buttons.append(
            InlineKeyboardButton(text=get_text('next', lang) + " ▶️",
                                 callback_data=f"orders_filter_{filter_type}_{page + 1}")
        )

    if nav_buttons:
        buttons.append(nav_buttons)

    # Filtrlarni o'zgartirish
    buttons.append([
        InlineKeyboardButton(text=get_text('change_filter', lang),
                             callback_data="admin_orders_list")
    ])

    # Admin menyuga qaytish
    buttons.append([
        InlineKeyboardButton(text=get_text('back', lang),
                             callback_data="back_to_admin")
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_orders_filter_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Buyurtmalarni filtrlash klaviaturasi
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('filter_all', lang),
                                 callback_data="orders_filter_all_0")
        ],
        [
            InlineKeyboardButton(text=get_text('filter_new', lang),
                                 callback_data="orders_filter_new_0"),
            InlineKeyboardButton(text=get_text('filter_processing', lang),
                                 callback_data="orders_filter_processing_0")
        ],
        [
            InlineKeyboardButton(text=get_text('filter_delivering', lang),
                                 callback_data="orders_filter_delivering_0"),
            InlineKeyboardButton(text=get_text('filter_completed', lang),
                                 callback_data="orders_filter_completed_0")
        ],
        [
            InlineKeyboardButton(text=get_text('filter_today', lang),
                                 callback_data="orders_filter_today_0"),
            InlineKeyboardButton(text=get_text('filter_week', lang),
                                 callback_data="orders_filter_week_0")
        ],
        [
            InlineKeyboardButton(text=get_text('back', lang),
                                 callback_data="back_to_admin")
        ]
    ])
    return keyboard


def get_order_detail_keyboard(order_id: int, current_status: str,
                              lang: str) -> InlineKeyboardMarkup:
    """
    Buyurtma tafsilotlari klaviaturasi
    """
    buttons = []

    # Status o'zgartirish tugmalari
    status_buttons = []

    if current_status == 'new':
        status_buttons.append([
            InlineKeyboardButton(text=get_text('status_processing', lang),
                                 callback_data=f"update_status_{order_id}_processing")
        ])

    if current_status == 'processing':
        status_buttons.append([
            InlineKeyboardButton(text=get_text('status_delivering', lang),
                                 callback_data=f"update_status_{order_id}_delivering")
        ])

    if current_status == 'delivering':
        status_buttons.append([
            InlineKeyboardButton(text=get_text('status_completed', lang),
                                 callback_data=f"update_status_{order_id}_completed")
        ])

    if current_status not in ['completed', 'cancelled']:
        status_buttons.append([
            InlineKeyboardButton(text=get_text('status_cancelled', lang),
                                 callback_data=f"update_status_{order_id}_cancelled")
        ])

    buttons.extend(status_buttons)

    # Orqaga qaytish
    buttons.append([
        InlineKeyboardButton(text=get_text('back', lang),
                             callback_data="admin_orders_list")
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_edit_product_keyboard(product_id: int, lang: str) -> InlineKeyboardMarkup:
    """
    Mahsulotni tahrirlash klaviaturasi
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('edit_name', lang),
                                 callback_data=f"edit_product_name_{product_id}")
        ],
        [
            InlineKeyboardButton(text=get_text('edit_price', lang),
                                 callback_data=f"edit_product_price_{product_id}")
        ],
        [
            InlineKeyboardButton(text=get_text('edit_description', lang),
                                 callback_data=f"edit_product_desc_{product_id}")
        ],
        [
            InlineKeyboardButton(text=get_text('delete', lang),
                                 callback_data=f"delete_product_{product_id}")
        ],
        [
            InlineKeyboardButton(text=get_text('back', lang),
                                 callback_data="admin_products_list")
        ]
    ])
    return keyboard


def get_statistics_filter_keyboard(lang: str, show_back: bool = False) -> InlineKeyboardMarkup:
    """
    Statistika vaqt filtrini tanlash klaviaturasi
    """
    buttons = [
        [
            InlineKeyboardButton(text=get_text('filter_all', lang),
                                 callback_data="stats_all")
        ],
        [
            InlineKeyboardButton(text=get_text('filter_today', lang),
                                 callback_data="stats_today"),
            InlineKeyboardButton(text=get_text('filter_week', lang),
                                 callback_data="stats_week")
        ],
        [
            InlineKeyboardButton(text=get_text('filter_month', lang),
                                 callback_data="stats_month")
        ]
    ]

    if show_back:
        buttons.append([
            InlineKeyboardButton(text=get_text('back', lang),
                                 callback_data="back_to_admin")
        ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_cancel_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Bekor qilish klaviaturasi
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('cancel', lang),
                                 callback_data="cancel_admin_action")
        ]
    ])
    return keyboard