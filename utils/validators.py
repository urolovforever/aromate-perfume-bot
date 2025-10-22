# utils/validators.py
"""
Ma'lumotlarni tekshirish funksiyalari
"""

import re
from typing import Optional


def validate_price(price_str: str) -> Optional[float]:
    """
    Narxni tekshirish va float ga o'tkazish
    """
    try:
        # Bo'sh joylarni olib tashlash
        price_str = price_str.strip().replace(' ', '').replace(',', '')

        # Faqat raqamlarni qabul qilish
        price = float(price_str)

        # Manfiy yoki 0 dan kichik bo'lmasligi kerak
        if price <= 0:
            return None

        return price
    except (ValueError, AttributeError):
        return None


def validate_phone(phone: str) -> bool:
    """
    Telefon raqamini tekshirish
    Format: +998XXXXXXXXX yoki 998XXXXXXXXX
    """
    # Bo'sh joylar va maxsus belgilarni olib tashlash
    phone = re.sub(r'[^\d+]', '', phone)

    # O'zbekiston raqami ekanligini tekshirish
    pattern = r'^(\+?998)?[0-9]{9}$'

    return bool(re.match(pattern, phone))


def validate_image(file_id: str) -> bool:
    """
    Telegram file_id ni tekshirish
    """
    # File_id bo'sh bo'lmasligi kerak
    if not file_id or len(file_id) < 10:
        return False

    return True


def validate_text_length(text: str, min_length: int = 3, max_length: int = 1000) -> bool:
    """
    Matn uzunligini tekshirish
    """
    if not text:
        return False

    text_len = len(text.strip())

    return min_length <= text_len <= max_length


def validate_caption_length(text: str, max_length: int = 1024) -> bool:
    """
    Telegram caption uzunligini tekshirish (max 1024 belgi)
    """
    if not text:
        return True  # Bo'sh caption ruxsat etiladi

    return len(text) <= max_length


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Matnni qisqartirish
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def validate_category(category: str) -> bool:
    """
    Kategoriya to'g'riligini tekshirish
    """
    valid_categories = ['men', 'women', 'unisex']
    return category in valid_categories


def validate_payment_type(payment_type: str) -> bool:
    """
    To'lov turini tekshirish
    """
    valid_types = ['cash', 'click', 'payme']
    return payment_type in valid_types


def validate_order_status(status: str) -> bool:
    """
    Buyurtma statusini tekshirish
    """
    valid_statuses = ['new', 'processing', 'delivering', 'completed', 'cancelled']
    return status in valid_statuses


def sanitize_text(text: str) -> str:
    """
    Matnni tozalash (HTML teglarni olib tashlash)
    """
    # HTML teglarni olib tashlash
    text = re.sub(r'<[^>]+>', '', text)

    # Ortiqcha bo'sh joylarni olib tashlash
    text = ' '.join(text.split())

    return text.strip()


def format_phone(phone: str) -> str:
    """
    Telefon raqamini formatlash
    """
    # Faqat raqamlarni qoldirish
    phone = re.sub(r'\D', '', phone)

    # +998 bilan boshlash
    if phone.startswith('998'):
        phone = '+' + phone
    elif not phone.startswith('+998'):
        phone = '+998' + phone

    return phone


def format_price(price: float) -> str:
    """
    Narxni formatlash (1000 -> 1 000)
    """
    return f"{price:,.0f}".replace(',', ' ')