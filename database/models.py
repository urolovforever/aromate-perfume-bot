# database/models.py
"""
SQLAlchemy ORM modellari
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """
    Foydalanuvchilar jadvali
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False, index=True)  # Telegram user_id
    username = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=False)
    language = Column(String(2), default='uz')  # uz yoki ru
    is_admin = Column(Boolean, default=False)
    role = Column(String(20), default='user')  # user, operator, admin, superadmin
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    cart_items = relationship("Cart", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, full_name='{self.full_name}')>"


class Product(Base):
    """
    Mahsulotlar jadvali
    """
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name_uz = Column(String(255), nullable=False)
    name_ru = Column(String(255), nullable=False)
    description_uz = Column(Text, nullable=False)
    description_ru = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)  # men, women, unisex
    image_url = Column(String(500), nullable=False)  # Telegram file_id
    stock_quantity = Column(Integer, default=0)  # Ombordagi miqdor
    low_stock_threshold = Column(Integer, default=5)  # Kam qolganda ogohlantirish
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    cart_items = relationship("Cart", back_populates="product", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="product")
    inventory_logs = relationship("InventoryLog", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product(id={self.id}, name_uz='{self.name_uz}', stock={self.stock_quantity})>"


class InventoryLog(Base):
    """
    Ombor o'zgarishlari loglari
    """
    __tablename__ = 'inventory_logs'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    admin_id = Column(Integer, nullable=False)  # Kim o'zgartirdi
    admin_username = Column(String(255), nullable=True)
    change_type = Column(String(20), nullable=False)  # manual_add, manual_remove, order_sold, order_cancelled
    quantity_before = Column(Integer, nullable=False)
    quantity_after = Column(Integer, nullable=False)
    change_amount = Column(Integer, nullable=False)  # +10 yoki -5
    reason = Column(Text, nullable=True)  # Sabab
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="inventory_logs")

    def __repr__(self):
        return f"<InventoryLog(product_id={self.product_id}, change={self.change_amount})>"


class Cart(Base):
    """
    Savat (savatcha) jadvali
    """
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

    def __repr__(self):
        return f"<Cart(user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity})>"


class Order(Base):
    """
    Buyurtmalar jadvali
    """
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(Text, nullable=False)
    payment_type = Column(String(20), nullable=False)  # cash, click, payme
    total = Column(Float, nullable=False)
    status = Column(String(20), default='new')  # new, processing, delivering, completed, cancelled
    is_paid = Column(Boolean, default=False)
    operator_id = Column(Integer, nullable=True)  # Qaysi operator sotgani
    operator_username = Column(String(255), nullable=True)  # Operator username
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, total={self.total}, status='{self.status}')>"


class OrderItem(Base):
    """
    Buyurtma mahsulotlari jadvali
    """
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product_name = Column(String(255), nullable=False)  # Mahsulot nomi o'chirilsa ham saqlansin
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)  # Buyurtma paytidagi narx

    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem(order_id={self.order_id}, product_name='{self.product_name}', quantity={self.quantity})>"