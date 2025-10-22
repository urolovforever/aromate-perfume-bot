# config.py
"""
Bot konfiguratsiyasi va sozlamalar
"""

import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

# Bot tokeni
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///atir_bot.db")

# Admin ID lar (vergul bilan ajratilgan)
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(admin_id.strip()) for admin_id in ADMIN_IDS_STR.split(",") if admin_id.strip()]

# Super Admin ID (faqat bitta, to'liq huquq)
SUPER_ADMIN_ID = os.getenv("SUPER_ADMIN_ID", "")
if SUPER_ADMIN_ID:
    SUPER_ADMIN_ID = int(SUPER_ADMIN_ID)
else:
    SUPER_ADMIN_ID = None

# Operatorlar guruhi ID
OPERATORS_GROUP_ID = os.getenv("OPERATORS_GROUP_ID", "-1003114367481")
if OPERATORS_GROUP_ID:
    OPERATORS_GROUP_ID = int(OPERATORS_GROUP_ID)
else:
    OPERATORS_GROUP_ID = None

# Default til
DEFAULT_LANGUAGE = "uz"

# Sahifa bo'yicha mahsulotlar soni
PRODUCTS_PER_PAGE = 5

# Click va Payme sozlamalari (ixtiyoriy)
CLICK_MERCHANT_ID = os.getenv("CLICK_MERCHANT_ID", "")
CLICK_SERVICE_ID = os.getenv("CLICK_SERVICE_ID", "")
CLICK_SECRET_KEY = os.getenv("CLICK_SECRET_KEY", "")

PAYME_MERCHANT_ID = os.getenv("PAYME_MERCHANT_ID", "")
PAYME_SECRET_KEY = os.getenv("PAYME_SECRET_KEY", "")

# Bot obyekti (global, handlers uchun kerak)
BOT = None

# Logging sozlamalari
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)