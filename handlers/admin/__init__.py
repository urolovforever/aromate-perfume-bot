# handlers/admin/__init__.py
"""
Admin uchun barcha handlerlar
"""

from .panel import admin_panel_router
from .add_product import add_product_router
from .operator import operator_router

__all__ = [
    'admin_panel_router',
    'add_product_router',
    'operator_router'
]