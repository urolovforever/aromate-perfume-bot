# database/db.py
"""
Database bilan ishlash funksiyalari
"""

from sqlalchemy import create_engine, select, and_, func
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List, Dict
from datetime import datetime

from .models import Base, User, Product, Cart, Order, OrderItem
from config import DATABASE_URL

# Engine va session yaratish
engine = create_engine(DATABASE_URL, echo=False)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


async def init_db():
    """
    Database jadvalllarini yaratish
    """
    Base.metadata.create_all(engine)
    print("✅ Database initialized successfully!")


# ==================== USER FUNCTIONS ====================

async def get_user(user_id: int) -> Optional[Dict]:
    """
    Foydalanuvchini olish
    """
    try:
        session = Session()
        user = session.query(User).filter(User.user_id == user_id).first()

        if user:
            return {
                'id': user.id,
                'user_id': user.user_id,
                'username': user.username,
                'full_name': user.full_name,
                'language': user.language,
                'is_admin': user.is_admin,
                'role': user.role if hasattr(user, 'role') else 'user',
                'created_at': user.created_at.strftime('%Y-%m-%d %H:%M')
            }
        return None
    except SQLAlchemyError as e:
        print(f"❌ Error getting user: {e}")
        return None
    finally:
        Session.remove()


async def create_user(user_id: int, username: str, full_name: str, language: str = 'uz') -> bool:
    """
    Yangi foydalanuvchi yaratish
    """
    try:
        session = Session()

        # Foydalanuvchi mavjudligini tekshirish
        existing_user = session.query(User).filter(User.user_id == user_id).first()
        if existing_user:
            return True

        new_user = User(
            user_id=user_id,
            username=username,
            full_name=full_name,
            language=language
        )

        session.add(new_user)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Error creating user: {e}")
        return False
    finally:
        Session.remove()


async def update_user_language(user_id: int, language: str) -> bool:
    """
    Foydalanuvchi tilini yangilash
    """
    try:
        session = Session()
        user = session.query(User).filter(User.user_id == user_id).first()

        if user:
            user.language = language
            session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Error updating language: {e}")
        return False
    finally:
        Session.remove()


async def get_admins() -> List[int]:
    """
    Admin foydalanuvchilarni olish
    """
    try:
        session = Session()
        admins = session.query(User.user_id).filter(User.is_admin == True).all()
        return [admin[0] for admin in admins]
    except SQLAlchemyError as e:
        print(f"❌ Error getting admins: {e}")
        return []
    finally:
        Session.remove()


# ==================== PRODUCT FUNCTIONS ====================

async def get_products_by_category(category: str, lang: str) -> List[Dict]:
    """
    Kategoriya bo'yicha mahsulotlarni olish
    """
    try:
        session = Session()
        products = session.query(Product).filter(
            and_(Product.category == category, Product.is_active == True)
        ).all()

        result = []
        for product in products:
            result.append({
                'id': product.id,
                'name': product.name_uz if lang == 'uz' else product.name_ru,
                'description': product.description_uz if lang == 'uz' else product.description_ru,
                'price': product.price,
                'category': product.category,
                'image_url': product.image_url
            })

        return result
    except SQLAlchemyError as e:
        print(f"❌ Error getting products: {e}")
        return []
    finally:
        Session.remove()


async def get_product_by_id(product_id: int, lang: str) -> Optional[Dict]:
    """
    ID bo'yicha mahsulotni olish
    """
    try:
        session = Session()
        product = session.query(Product).filter(Product.id == product_id).first()

        if product:
            return {
                'id': product.id,
                'name': product.name_uz if lang == 'uz' else product.name_ru,
                'description': product.description_uz if lang == 'uz' else product.description_ru,
                'price': product.price,
                'category': product.category,
                'image_url': product.image_url
            }
        return None
    except SQLAlchemyError as e:
        print(f"❌ Error getting product: {e}")
        return None
    finally:
        Session.remove()


async def get_all_products() -> List[Dict]:
    """
    Barcha mahsulotlarni olish (admin uchun)
    """
    try:
        session = Session()
        products = session.query(Product).filter(Product.is_active == True).all()

        result = []
        for product in products:
            result.append({
                'id': product.id,
                'name_uz': product.name_uz,
                'name_ru': product.name_ru,
                'price': product.price,
                'category': product.category,
                'image_url': product.image_url
            })

        return result
    except SQLAlchemyError as e:
        print(f"❌ Error getting all products: {e}")
        return []
    finally:
        Session.remove()


async def create_product(name_uz: str, name_ru: str, description_uz: str,
                         description_ru: str, price: float, category: str,
                         image_url: str) -> Optional[Dict]:
    """
    Yangi mahsulot yaratish
    """
    try:
        session = Session()

        new_product = Product(
            name_uz=name_uz,
            name_ru=name_ru,
            description_uz=description_uz,
            description_ru=description_ru,
            price=price,
            category=category,
            image_url=image_url
        )

        session.add(new_product)
        session.commit()
        session.refresh(new_product)

        return {
            'id': new_product.id,
            'name_uz': new_product.name_uz,
            'name_ru': new_product.name_ru,
            'price': new_product.price
        }
    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Error creating product: {e}")
        return None
    finally:
        Session.remove()


async def delete_product(product_id: int) -> bool:
    """
    Mahsulotni o'chirish (soft delete)
    """
    try:
        session = Session()
        product = session.query(Product).filter(Product.id == product_id).first()

        if product:
            product.is_active = False
            session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Error deleting product: {e}")
        return False
    finally:
        Session.remove()


# ==================== CART FUNCTIONS ====================

async def add_to_cart(user_id: int, product_id: int, quantity: int = 1) -> bool:
    """
    Savatga mahsulot qo'shish
    """
    try:
        session = Session()

        # Savatda mavjudligini tekshirish
        cart_item = session.query(Cart).filter(
            and_(Cart.user_id == user_id, Cart.product_id == product_id)
        ).first()

        if cart_item:
            # Agar mavjud bo'lsa, miqdorni oshirish
            cart_item.quantity += quantity
        else:
            # Yangi qo'shish
            new_cart_item = Cart(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity
            )
            session.add(new_cart_item)

        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Error adding to cart: {e}")
        return False
    finally:
        Session.remove()


async def get_cart_items(user_id: int, lang: str) -> List[Dict]:
    """
    Foydalanuvchi savatidagi mahsulotlarni olish
    """
    try:
        session = Session()
        cart_items = session.query(Cart, Product).join(Product).filter(
            Cart.user_id == user_id
        ).all()

        result = []
        for cart, product in cart_items:
            result.append({
                'cart_id': cart.id,
                'product_id': product.id,
                'name': product.name_uz if lang == 'uz' else product.name_ru,
                'price': product.price,
                'quantity': cart.quantity,
                'image_url': product.image_url
            })

        return result
    except SQLAlchemyError as e:
        print(f"❌ Error getting cart items: {e}")
        return []
    finally:
        Session.remove()


async def get_cart_item_by_id(cart_item_id: int, user_id: int, lang: str) -> Optional[Dict]:
    """
    ID bo'yicha savat mahsulotini olish
    """
    try:
        session = Session()
        cart_item = session.query(Cart, Product).join(Product).filter(
            and_(Cart.id == cart_item_id, Cart.user_id == user_id)
        ).first()

        if cart_item:
            cart, product = cart_item
            return {
                'cart_id': cart.id,
                'product_id': product.id,
                'name': product.name_uz if lang == 'uz' else product.name_ru,
                'price': product.price,
                'quantity': cart.quantity,
                'image_url': product.image_url
            }
        return None
    except SQLAlchemyError as e:
        print(f"❌ Error getting cart item: {e}")
        return None
    finally:
        Session.remove()


async def update_cart_quantity(cart_item_id: int, user_id: int, change: int) -> bool:
    """
    Savat mahsuloti miqdorini o'zgartirish
    change: +1 (oshirish) yoki -1 (kamaytirish)
    """
    try:
        session = Session()
        cart_item = session.query(Cart).filter(
            and_(Cart.id == cart_item_id, Cart.user_id == user_id)
        ).first()

        if cart_item:
            cart_item.quantity += change

            # Agar miqdor 0 ga teng yoki kichik bo'lsa, o'chirish
            if cart_item.quantity <= 0:
                session.delete(cart_item)

            session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Error updating cart quantity: {e}")
        return False
    finally:
        Session.remove()


async def remove_from_cart(cart_item_id: int, user_id: int) -> bool:
    """
    Savatdan mahsulotni o'chirish
    """
    try:
        session = Session()
        cart_item = session.query(Cart).filter(
            and_(Cart.id == cart_item_id, Cart.user_id == user_id)
        ).first()

        if cart_item:
            session.delete(cart_item)
            session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Error removing from cart: {e}")
        return False
    finally:
        Session.remove()


async def clear_cart(user_id: int) -> bool:
    """
    Savatni tozalash
    """
    try:
        session = Session()
        session.query(Cart).filter(Cart.user_id == user_id).delete()
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Error clearing cart: {e}")
        return False
    finally:
        Session.remove()


# ==================== ORDER FUNCTIONS ====================

async def create_order(user_id: int, phone: str, address: str,
                       payment_type: str, cart_items: List[Dict],
                       total: float) -> Optional[Dict]:
    """
    Buyurtma yaratish
    """
    try:
        session = Session()

        # To'lov qilinganligi (Click/Payme uchun keyinchalik TRUE qilinadi)
        is_paid = False
        if payment_type in ['click', 'payme']:
            # Bu yerda to'lov integratsiyasi bo'lishi kerak
            # Hozircha FALSE qoldiramiz
            pass

        # Buyurtma yaratish
        new_order = Order(
            user_id=user_id,
            phone=phone,
            address=address,
            payment_type=payment_type,
            total=total,
            is_paid=is_paid
        )

        session.add(new_order)
        session.flush()  # ID ni olish uchun

        # Buyurtma mahsulotlarini qo'shish
        for item in cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item['product_id'],
                product_name=item['name'],
                quantity=item['quantity'],
                price=item['price']
            )
            session.add(order_item)

        session.commit()
        session.refresh(new_order)

        return {
            'id': new_order.id,
            'total': new_order.total,
            'status': new_order.status,
            'is_paid': new_order.is_paid
        }
    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Error creating order: {e}")
        return None
    finally:
        Session.remove()


async def get_all_orders() -> List[Dict]:
    """
    Barcha buyurtmalarni olish (admin uchun)
    """
    try:
        session = Session()
        orders = session.query(Order, User).join(User).order_by(Order.created_at.desc()).all()

        result = []
        for order, user in orders:
            result.append({
                'id': order.id,
                'user_id': order.user_id,
                'user_name': user.full_name,
                'phone': order.phone,
                'total': order.total,
                'status': order.status,
                'is_paid': order.is_paid,
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M')
            })

        return result
    except SQLAlchemyError as e:
        print(f"❌ Error getting orders: {e}")
        return []
    finally:
        Session.remove()


async def get_orders_by_filter(filter_type: str = 'all') -> List[Dict]:
    """
    Filtrlangan buyurtmalarni olish
    filter_type: all, new, processing, delivering, completed, today, week
    """
    try:
        session = Session()
        query = session.query(Order, User).join(User)

        # Status bo'yicha filtrlash
        if filter_type == 'new':
            query = query.filter(Order.status == 'new')
        elif filter_type == 'processing':
            query = query.filter(Order.status == 'processing')
        elif filter_type == 'delivering':
            query = query.filter(Order.status == 'delivering')
        elif filter_type == 'completed':
            query = query.filter(Order.status == 'completed')
        elif filter_type == 'today':
            from datetime import date
            today = date.today()
            query = query.filter(func.date(Order.created_at) == today)
        elif filter_type == 'week':
            from datetime import datetime, timedelta
            week_ago = datetime.now() - timedelta(days=7)
            query = query.filter(Order.created_at >= week_ago)
        # all uchun hech qanday filtr qo'shmaymiz

        orders = query.order_by(Order.created_at.desc()).all()

        result = []
        for order, user in orders:
            result.append({
                'id': order.id,
                'user_id': order.user_id,
                'user_name': user.full_name,
                'phone': order.phone,
                'total': order.total,
                'status': order.status,
                'is_paid': order.is_paid,
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M')
            })

        return result
    except SQLAlchemyError as e:
        print(f"❌ Error getting filtered orders: {e}")
        return []
    finally:
        Session.remove()


async def get_order_by_id(order_id: int) -> Optional[Dict]:
    """
    Buyurtmani ID bo'yicha olish
    """
    try:
        session = Session()
        order = session.query(Order, User).join(User).filter(Order.id == order_id).first()

        if not order:
            return None

        order_obj, user = order

        # Buyurtma mahsulotlarini olish
        items = session.query(OrderItem).filter(OrderItem.order_id == order_id).all()

        items_list = []
        for item in items:
            items_list.append({
                'product_id': item.product_id,
                'name': item.product_name,
                'quantity': item.quantity,
                'price': item.price
            })

        return {
            'id': order_obj.id,
            'user_id': order_obj.user_id,
            'user_name': user.full_name,
            'phone': order_obj.phone,
            'address': order_obj.address,
            'payment_type': order_obj.payment_type,
            'total': order_obj.total,
            'status': order_obj.status,
            'is_paid': order_obj.is_paid,
            'operator_id': order_obj.operator_id,
            'operator_username': order_obj.operator_username,
            'created_at': order_obj.created_at.strftime('%Y-%m-%d %H:%M'),
            'items': items_list
        }
    except SQLAlchemyError as e:
        print(f"❌ Error getting order: {e}")
        return None
    finally:
        Session.remove()


async def update_order_status(order_id: int, new_status: str) -> bool:
    """
    Buyurtma statusini yangilash
    """
    try:
        session = Session()
        order = session.query(Order).filter(Order.id == order_id).first()

        if order:
            order.status = new_status
            order.updated_at = datetime.utcnow()

            # Agar status 'completed' bo'lsa, to'landi deb belgilash
            if new_status == 'completed':
                order.is_paid = True

            session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Error updating order status: {e}")
        return False
    finally:
        Session.remove()


async def assign_operator_to_order(order_id: int, operator_id: int, operator_username: str) -> bool:
    """
    Buyurtmaga operator tayinlash
    """
    try:
        session = Session()
        order = session.query(Order).filter(Order.id == order_id).first()

        if order and not order.operator_id:
            order.operator_id = operator_id
            order.operator_username = operator_username
            session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Error assigning operator: {e}")
        return False
    finally:
        Session.remove()


async def get_operator_statistics(operator_id: int, period: str = 'all') -> Dict:
    """
    Operator statistikasi
    period: all, today, week, month
    """
    try:
        session = Session()
        query = session.query(Order).filter(Order.operator_id == operator_id)

        # Vaqt bo'yicha filtrlash
        if period == 'today':
            from datetime import date
            today = date.today()
            query = query.filter(func.date(Order.created_at) == today)
        elif period == 'week':
            from datetime import datetime, timedelta
            week_ago = datetime.now() - timedelta(days=7)
            query = query.filter(Order.created_at >= week_ago)
        elif period == 'month':
            from datetime import datetime, timedelta
            month_ago = datetime.now() - timedelta(days=30)
            query = query.filter(Order.created_at >= month_ago)

        total_orders = query.count()
        completed_orders = query.filter(Order.status == 'completed').count()
        total_revenue = query.filter(Order.status == 'completed').with_entities(func.sum(Order.total)).scalar() or 0

        return {
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'total_revenue': total_revenue
        }
    except SQLAlchemyError as e:
        print(f"❌ Error getting operator statistics: {e}")
        return {
            'total_orders': 0,
            'completed_orders': 0,
            'total_revenue': 0
        }
    finally:
        Session.remove()


# ==================== STATISTICS FUNCTIONS ====================

async def get_statistics(period: str = 'all') -> Dict:
    """
    Statistika ma'lumotlari
    period: all, today, week, month
    """
    try:
        session = Session()

        # Vaqt bo'yicha filtrlash uchun base query
        orders_query = session.query(Order)

        if period == 'today':
            from datetime import date
            today = date.today()
            orders_query = orders_query.filter(func.date(Order.created_at) == today)
        elif period == 'week':
            from datetime import datetime, timedelta
            week_ago = datetime.now() - timedelta(days=7)
            orders_query = orders_query.filter(Order.created_at >= week_ago)
        elif period == 'month':
            from datetime import datetime, timedelta
            month_ago = datetime.now() - timedelta(days=30)
            orders_query = orders_query.filter(Order.created_at >= month_ago)

        total_users = session.query(func.count(User.id)).scalar()
        total_products = session.query(func.count(Product.id)).filter(Product.is_active == True).scalar()
        total_orders = orders_query.count()
        completed_orders = orders_query.filter(Order.status == 'completed').count()
        pending_orders = orders_query.filter(Order.status.in_(['new', 'processing'])).count()
        total_revenue = orders_query.filter(Order.status == 'completed').with_entities(
            func.sum(Order.total)).scalar() or 0

        # Top operatorlar
        top_operators = session.query(
            Order.operator_username,
            func.count(Order.id).label('order_count'),
            func.sum(Order.total).label('revenue')
        ).filter(
            Order.operator_id.isnot(None),
            Order.status == 'completed'
        ).group_by(Order.operator_username).order_by(func.sum(Order.total).desc()).limit(5).all()

        operators_list = []
        for operator in top_operators:
            operators_list.append({
                'username': operator[0],
                'orders': operator[1],
                'revenue': operator[2] or 0
            })

        return {
            'total_users': total_users,
            'total_products': total_products,
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'pending_orders': pending_orders,
            'total_revenue': total_revenue,
            'top_operators': operators_list
        }
    except SQLAlchemyError as e:
        print(f"❌ Error getting statistics: {e}")
        return {
            'total_users': 0,
            'total_products': 0,
            'total_orders': 0,
            'completed_orders': 0,
            'pending_orders': 0,
            'total_revenue': 0,
            'top_operators': []
        }
    finally:
        Session.remove()