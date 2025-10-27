# handlers/__init__.py
"""
Barcha handlerlarni shu yerda import qilamiz va ro'yxatga olamiz
"""

from .user.start import start_router
from .user.menu import menu_router
from .user.product import product_router
from .user.cart import cart_router
from .admin.panel import admin_panel_router
from .admin.add_product import add_product_router
from .admin.inventory import inventory_router
from .admin.operator import operator_router


# Barcha routerlarni bitta ro'yxatga yig'amiz
def register_all_handlers(dp):
    """
    Barcha handlerlarni dispatcher ga qo'shish
    """
    # User handlerlar
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(product_router)
    dp.include_router(cart_router)

    # Admin handlerlar
    dp.include_router(admin_panel_router)
    dp.include_router(add_product_router)
    dp.include_router(inventory_router)

    # Operator handlerlar
    dp.include_router(operator_router)