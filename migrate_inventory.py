#!/usr/bin/env python3
"""
Database migration script for inventory management system
Adds stock_quantity and low_stock_threshold fields to products table
Creates product_ml_variants table
"""

import sqlite3
import sys

def migrate_database(db_path='atir_bot.db'):
    """
    Database ni yangilash
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("🔄 Starting database migration...")

        # Check if columns already exist
        cursor.execute("PRAGMA table_info(products)")
        columns = [column[1] for column in cursor.fetchall()]

        # Add stock_quantity column if not exists
        if 'stock_quantity' not in columns:
            cursor.execute("""
                ALTER TABLE products
                ADD COLUMN stock_quantity INTEGER DEFAULT 0 NOT NULL
            """)
            print("✅ Added stock_quantity column to products table")
        else:
            print("ℹ️  stock_quantity column already exists")

        # Add low_stock_threshold column if not exists
        if 'low_stock_threshold' not in columns:
            cursor.execute("""
                ALTER TABLE products
                ADD COLUMN low_stock_threshold INTEGER DEFAULT 5 NOT NULL
            """)
            print("✅ Added low_stock_threshold column to products table")
        else:
            print("ℹ️  low_stock_threshold column already exists")

        # Create product_ml_variants table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_ml_variants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                ml_amount INTEGER NOT NULL,
                price REAL NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """)
        print("✅ Created product_ml_variants table")

        # Check if order_items table needs updates
        cursor.execute("PRAGMA table_info(order_items)")
        order_columns = [column[1] for column in cursor.fetchall()]

        # Add variant_type column if not exists
        if 'variant_type' not in order_columns:
            cursor.execute("""
                ALTER TABLE order_items
                ADD COLUMN variant_type TEXT
            """)
            print("✅ Added variant_type column to order_items table")
        else:
            print("ℹ️  variant_type column already exists")

        # Add ml_variant_id column if not exists
        if 'ml_variant_id' not in order_columns:
            cursor.execute("""
                ALTER TABLE order_items
                ADD COLUMN ml_variant_id INTEGER
            """)
            print("✅ Added ml_variant_id column to order_items table")
        else:
            print("ℹ️  ml_variant_id column already exists")

        conn.commit()
        print("✅ Database migration completed successfully!")

        # Show current products count
        cursor.execute("SELECT COUNT(*) FROM products WHERE is_active = 1")
        products_count = cursor.fetchone()[0]
        print(f"📊 Active products: {products_count}")

        conn.close()

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    # Get database path from command line or use default
    db_path = sys.argv[1] if len(sys.argv) > 1 else 'atir_bot.db'
    migrate_database(db_path)
