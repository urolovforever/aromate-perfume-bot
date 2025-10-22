# migrate_database.py
"""
Database ni yangilash uchun migration script
Agar database allaqachon mavjud bo'lsa, yangi ustunlarni qo'shadi
"""

import sqlite3
import os


def migrate_database():
    """
    Orders jadvaliga operator ustunlarini qo'shish
    """
    db_path = "atir_bot.db"

    if not os.path.exists(db_path):
        print("❌ Database fayli topilmadi. Avval botni ishga tushiring.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Orders jadvalidagi ustunlarni tekshirish
        cursor.execute("PRAGMA table_info(orders)")
        columns = [column[1] for column in cursor.fetchall()]

        # operator_id ustuni yo'qligini tekshirish
        if 'operator_id' not in columns:
            print("➕ operator_id ustunini qo'shish...")
            cursor.execute("ALTER TABLE orders ADD COLUMN operator_id INTEGER")
            print("✅ operator_id ustuni qo'shildi")
        else:
            print("ℹ️ operator_id ustuni allaqachon mavjud")

        # operator_username ustuni yo'qligini tekshirish
        if 'operator_username' not in columns:
            print("➕ operator_username ustunini qo'shish...")
            cursor.execute("ALTER TABLE orders ADD COLUMN operator_username VARCHAR(255)")
            print("✅ operator_username ustuni qo'shildi")
        else:
            print("ℹ️ operator_username ustuni allaqachon mavjud")

        conn.commit()
        conn.close()

        print("\n✅ Migration muvaffaqiyatli yakunlandi!")

    except Exception as e:
        print(f"❌ Xatolik: {e}")
        if conn:
            conn.rollback()
            conn.close()


if __name__ == "__main__":
    print("🔄 Database migration boshlandi...\n")
    migrate_database()