# keyboards/__init__.py
"""
Barcha klaviaturalarni import qilish
"""

from .user_keyboards import (
    get_language_keyboard,
    get_main_menu_keyboard,
    get_products_list_keyboard,
    get_product_detail_keyboard,
    get_cart_keyboard,
    get_payment_keyboard,
    get_phone_request_keyboard,
    get_settings_keyboard,
    get_back_to_main_menu_keyboard,
    get_back_to_category_keyboard
)

from .admin_keyboards import (
    get_admin_menu_keyboard,
    get_category_selection_keyboard,
    get_confirm_product_keyboard,
    get_products_admin_keyboard,
    get_orders_keyboard,
    get_orders_filter_keyboard,
    get_order_detail_keyboard,
    get_statistics_filter_keyboard
)

__all__ = [
    # User keyboards
    'get_language_keyboard',
    'get_main_menu_keyboard',
    'get_products_list_keyboard',
    'get_product_detail_keyboard',
    'get_cart_keyboard',
    'get_payment_keyboard',
    'get_phone_request_keyboard',
    'get_settings_keyboard',
    'get_back_to_main_menu_keyboard',
    'get_back_to_category_keyboard',

    # Admin keyboards
    'get_admin_menu_keyboard',
    'get_category_selection_keyboard',
    'get_confirm_product_keyboard',
    'get_products_admin_keyboard',
    'get_orders_keyboard',
    'get_orders_filter_keyboard',
    'get_order_detail_keyboard'
]