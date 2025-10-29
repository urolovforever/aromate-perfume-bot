# bot.py
"""
Botni ishga tushirish asosiy fayli bu yerda
"""

import asyncio
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN, logger
import config
from database import init_db
from handlers import register_all_handlers


async def main():
    """
    Botni ishga tushirish
    """
    # Bot tokenini tekshirish
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN topilmadi! .env faylini tekshiring.")
        sys.exit(1)

    # Bot va Dispatcher yaratish
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Bot obyektini global qilish (handlers uchun)
    config.BOT = bot

    dp = Dispatcher()

    # Database ni ishga tushirish
    logger.info("📦 Database yaratilmoqda...")
    await init_db()

    # Handlerlarni ro'yxatga olish
    logger.info("🔧 Handlerlar ro'yxatga olinmoqda...")
    register_all_handlers(dp)

    # Botni ishga tushirish
    logger.info("🚀 Bot ishga tushdi!")

    try:
        # Polling boshlanishi
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"❌ Xatolik: {e}")
    finally:
        await bot.session.close()
        logger.info("👋 Bot to'xtatildi")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot to'xtatildi (KeyboardInterrupt)")
