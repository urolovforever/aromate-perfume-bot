# utils/decorators.py
"""
Yordamchi decoratorlar
"""

from functools import wraps
from aiogram.types import Message, CallbackQuery
from config import ADMIN_IDS, SUPER_ADMIN_ID


def admin_only(func):
    """
    Faqat adminlar uchun decorator (operator ham admin)
    """

    @wraps(func)
    async def wrapper(event, *args, **kwargs):
        # Message yoki CallbackQuery ekanligini aniqlash
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        else:
            return

        # Admin yoki Super Admin ekanligini tekshirish
        if user_id not in ADMIN_IDS and user_id != SUPER_ADMIN_ID:
            if isinstance(event, Message):
                await event.answer("❌ Sizda admin huquqi yo'q!")
            elif isinstance(event, CallbackQuery):
                await event.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
            return

        # Agar admin bo'lsa, funksiyani ishga tushirish
        return await func(event, *args, **kwargs)

    return wrapper


def superadmin_only(func):
    """
    Faqat super admin uchun decorator
    """

    @wraps(func)
    async def wrapper(event, *args, **kwargs):
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        else:
            return

        # Super admin ekanligini tekshirish
        if user_id != SUPER_ADMIN_ID:
            if isinstance(event, Message):
                await event.answer("❌ Bu funksiya faqat super admin uchun!")
            elif isinstance(event, CallbackQuery):
                await event.answer("❌ Bu funksiya faqat super admin uchun!", show_alert=True)
            return

        return await func(event, *args, **kwargs)

    return wrapper


async def can_modify_order(user_id: int, order_operator_id: int) -> bool:
    """
    Operatorning buyurtmani o'zgartirish huquqini tekshirish
    """
    # Super admin barchani o'zgartira oladi
    if user_id == SUPER_ADMIN_ID:
        return True

    # Operator faqat o'zining buyurtmasini o'zgartira oladi
    if user_id in ADMIN_IDS and order_operator_id == user_id:
        return True

    return False


def check_subscription(func):
    """
    Kanal obunasini tekshirish decorator (ixtiyoriy)
    """

    @wraps(func)
    async def wrapper(event, *args, **kwargs):
        # Bu yerda kanal obunasini tekshirish logikasi bo'lishi mumkin
        # Hozircha oddiy return qilamiz
        return await func(event, *args, **kwargs)

    return wrapper


def rate_limit(limit: int = 3):
    """
    Rate limiting decorator (spam oldini olish)
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(event, *args, **kwargs):
            # Bu yerda rate limiting logikasi bo'lishi mumkin
            # Redis yoki in-memory storage ishlatish mumkin
            return await func(event, *args, **kwargs)

        return wrapper

    return decorator