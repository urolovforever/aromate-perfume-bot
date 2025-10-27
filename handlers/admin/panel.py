# handlers/admin/panel.py
"""
Admin panel: statistika, mahsulotlar ro'yxati, buyurtmalar
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from database.db import (
    get_user, get_all_products, delete_product,
    get_all_orders, update_order_status, get_statistics
)
from keyboards.admin_keyboards import (
    get_admin_menu_keyboard,
    get_products_admin_keyboard,
    get_orders_keyboard,
    get_order_detail_keyboard
)
from utils.decorators import admin_only
from utils.localization import get_text

admin_panel_router = Router()


@admin_panel_router.message(Command("admin"))
@admin_only
async def admin_panel(message: Message):
    """
    Admin panel - faqat adminlar uchun
    """
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'uz')

    await message.answer(
        get_text('admin_welcome', lang),
        reply_markup=get_admin_menu_keyboard(lang)
    )


@admin_panel_router.callback_query(F.data == "admin_statistics")
@admin_only
async def show_statistics(callback: CallbackQuery):
    """
    Statistikani ko'rsatish - filtr tanlash
    """
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    from keyboards.admin_keyboards import get_statistics_filter_keyboard

    await callback.message.edit_text(
        get_text('select_statistics_period', lang),
        reply_markup=get_statistics_filter_keyboard(lang)
    )
    await callback.answer()


@admin_panel_router.callback_query(F.data.startswith("stats_"))
@admin_only
async def show_filtered_statistics(callback: CallbackQuery):
    """
    Filtrlangan statistikani ko'rsatish
    Format: stats_<period> (all, today, week, month)
    """
    period = callback.data.split("_")[1]
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    stats = await get_statistics(period)

    period_names = {
        'all': get_text('filter_all', lang),
        'today': get_text('filter_today', lang),
        'week': get_text('filter_week', lang),
        'month': get_text('filter_month', lang)
    }

    stats_text = get_text('statistics_title', lang) + f" ({period_names.get(period, '')})\n\n"
    stats_text += f"👥 {get_text('total_users', lang)}: {stats['total_users']}\n"
    stats_text += f"📦 {get_text('total_products', lang)}: {stats['total_products']}\n"
    stats_text += f"🛍️ {get_text('total_orders', lang)}: {stats['total_orders']}\n"
    stats_text += f"✅ {get_text('completed_orders', lang)}: {stats['completed_orders']}\n"
    stats_text += f"⏳ {get_text('pending_orders', lang)}: {stats['pending_orders']}\n"
    stats_text += f"💰 {get_text('total_revenue', lang)}: {stats['total_revenue']:,.0f} {get_text('sum', lang)}\n"

    # Top operatorlar
    if stats['top_operators']:
        stats_text += f"\n🏆 {get_text('top_operators', lang)}:\n"
        for idx, operator in enumerate(stats['top_operators'], 1):
            stats_text += f"{idx}. @{operator['username']}: {operator['orders']} ta / {operator['revenue']:,.0f} so'm\n"

    from keyboards.admin_keyboards import get_statistics_filter_keyboard

    await callback.message.edit_text(
        stats_text,
        reply_markup=get_statistics_filter_keyboard(lang, show_back=True)
    )
    await callback.answer()


@admin_panel_router.callback_query(F.data == "admin_products_list")
@admin_only
async def show_products_list(callback: CallbackQuery):
    """
    Mahsulotlar ro'yxatini ko'rsatish (tahrirlash va o'chirish uchun)
    """
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    products = await get_all_products()

    if not products:
        await callback.answer(get_text('no_products', lang), show_alert=True)
        return

    products_text = get_text('products_list_title', lang) + "\n\n"

    for product in products:
        products_text += f"🔹 {product['name_uz']} / {product['name_ru']}\n"
        products_text += f"   💰 {product['price']:,.0f} so'm\n"
        products_text += f"   📂 {product['category'].upper()}\n\n"

    await callback.message.edit_text(
        products_text,
        reply_markup=get_products_admin_keyboard(products, 0, lang)
    )
    await callback.answer()


@admin_panel_router.callback_query(F.data.startswith("delete_product_"))
@admin_only
async def delete_product_handler(callback: CallbackQuery):
    """
    Mahsulotni o'chirish
    Format: delete_product_<product_id>
    """
    product_id = int(callback.data.split("_")[2])
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    result = await delete_product(product_id)

    if result:
        await callback.answer(get_text('product_deleted', lang), show_alert=True)

        # Yangilangan ro'yxatni ko'rsatish
        products = await get_all_products()

        if not products:
            await callback.message.edit_text(
                get_text('no_products', lang),
                reply_markup=get_admin_menu_keyboard(lang)
            )
            return

        products_text = get_text('products_list_title', lang) + "\n\n"

        for product in products:
            products_text += f"🔹 {product['name_uz']} / {product['name_ru']}\n"
            products_text += f"   💰 {product['price']:,.0f} so'm\n"
            products_text += f"   📂 {product['category'].upper()}\n\n"

        await callback.message.edit_text(
            products_text,
            reply_markup=get_products_admin_keyboard(products, 0, lang)
        )
    else:
        await callback.answer(get_text('delete_error', lang), show_alert=True)


@admin_panel_router.callback_query(F.data == "admin_orders_list")
@admin_only
async def show_orders_list(callback: CallbackQuery):
    """
    Buyurtmalar ro'yxatini ko'rsatish - filtrlash menyusi
    """
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    from keyboards.admin_keyboards import get_orders_filter_keyboard

    await callback.message.edit_text(
        get_text('select_order_filter', lang),
        reply_markup=get_orders_filter_keyboard(lang)
    )
    await callback.answer()


@admin_panel_router.callback_query(F.data.startswith("orders_filter_"))
@admin_only
async def show_filtered_orders(callback: CallbackQuery):
    """
    Filtrlangan buyurtmalarni ko'rsatish
    Format: orders_filter_<filter_type>_<page>
    """
    from database.db import get_orders_by_filter

    data = callback.data.split("_")
    filter_type = data[2]  # all, new, processing, delivering, completed
    page = int(data[3]) if len(data) > 3 else 0

    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    orders = await get_orders_by_filter(filter_type)

    if not orders:
        await callback.answer(get_text('no_orders', lang), show_alert=True)
        return

    # Pagination
    ITEMS_PER_PAGE = 10
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE

    orders_text = get_text('orders_list_title', lang) + f" ({filter_type.upper()})\n\n"

    status_emoji = {
        'new': '🆕',
        'processing': '⏳',
        'delivering': '🚚',
        'completed': '✅',
        'cancelled': '❌'
    }

    for order in orders[start_idx:end_idx]:
        orders_text += f"{status_emoji.get(order['status'], '📦')} Buyurtma #{order['id']}\n"
        orders_text += f"   👤 {order['user_name']}\n"
        orders_text += f"   💰 {order['total']:,.0f} so'm\n"
        orders_text += f"   📅 {order['created_at']}\n\n"

    orders_text += f"\n📄 Sahifa: {page + 1}/{(len(orders) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE}"

    await callback.message.edit_text(
        orders_text,
        reply_markup=get_orders_keyboard(orders, page, lang, filter_type)
    )
    await callback.answer()


@admin_panel_router.callback_query(F.data.startswith("order_detail_"))
@admin_only
async def show_order_detail(callback: CallbackQuery):
    """
    Buyurtma tafsilotlari
    Format: order_detail_<order_id>
    """
    from database.db import get_order_by_id

    order_id = int(callback.data.split("_")[2])
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    order = await get_order_by_id(order_id)

    if not order:
        await callback.answer(get_text('order_not_found', lang), show_alert=True)
        return

    status_text = {
        'new': get_text('status_new', lang),
        'processing': get_text('status_processing', lang),
        'delivering': get_text('status_delivering', lang),
        'completed': get_text('status_completed', lang),
        'cancelled': get_text('status_cancelled', lang)
    }

    payment_text = {
        'cash': get_text('payment_cash', lang),
        'click': 'Click',
        'payme': 'Payme'
    }

    order_text = f"📋 Buyurtma #{order['id']}\n\n"
    order_text += f"👤 {order['user_name']}\n"
    order_text += f"📞 {order['phone']}\n"
    order_text += f"📍 {order['address']}\n"
    order_text += f"💳 {payment_text.get(order['payment_type'], order['payment_type'])}\n"
    order_text += f"📊 {status_text.get(order['status'], order['status'])}\n"
    order_text += f"💰 {get_text('payment_status', lang)}: "
    order_text += f"{'✅ ' + get_text('paid', lang) if order['is_paid'] else '⏳ ' + get_text('not_paid', lang)}\n"

    # Operator ma'lumotini ko'rsatish
    if order.get('operator_username'):
        order_text += f"👨‍💼 Operator: @{order['operator_username']}\n"

    order_text += f"📅 {order['created_at']}\n\n"

    order_text += "📦 Mahsulotlar:\n"
    for idx, item in enumerate(order['items'], 1):
        order_text += f"{idx}. {item['name']} x {item['quantity']}\n"
        order_text += f"   {item['price']:,.0f} so'm\n"

    order_text += f"\n💵 Jami: {order['total']:,.0f} so'm"

    await callback.message.edit_text(
        order_text,
        reply_markup=get_order_detail_keyboard(order_id, order['status'], lang)
    )
    await callback.answer()


@admin_panel_router.callback_query(F.data.startswith("update_status_"))
@admin_only
async def update_status_handler(callback: CallbackQuery):
    """
    Buyurtma statusini yangilash
    Format: update_status_<order_id>_<new_status>
    """
    data = callback.data.split("_")
    order_id = int(data[2])
    new_status = data[3]

    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    # Buyurtmani olish (ombor kamaytirish uchun kerak)
    from database.db import get_order_by_id, reduce_product_stock
    order = await get_order_by_id(order_id)

    result = await update_order_status(order_id, new_status)

    if result:
        # Agar buyurtma yakunlangan bo'lsa, ombor miqdorini kamaytirish
        if new_status == 'completed' and order:
            for item in order['items']:
                # Faqat bottle (asosiy mahsulot) uchun ombor miqdorini kamaytirish
                variant_type = item.get('variant_type', 'bottle')
                if variant_type == 'bottle':
                    await reduce_product_stock(item['product_id'], item['quantity'])

            # Kam qolgan mahsulotlarni tekshirish va adminlarga xabar berish
            from handlers.admin.inventory import check_and_notify_low_stock
            await check_and_notify_low_stock(callback.bot, lang)

        await callback.answer(get_text('status_updated', lang), show_alert=True)

        # Yangilangan buyurtmani ko'rsatish
        order = await get_order_by_id(order_id)

        status_text = {
            'new': get_text('status_new', lang),
            'processing': get_text('status_processing', lang),
            'delivering': get_text('status_delivering', lang),
            'completed': get_text('status_completed', lang),
            'cancelled': get_text('status_cancelled', lang)
        }

        payment_text = {
            'cash': get_text('payment_cash', lang),
            'click': 'Click',
            'payme': 'Payme'
        }

        order_text = f"📋 Buyurtma #{order['id']}\n\n"
        order_text += f"👤 {order['user_name']}\n"
        order_text += f"📞 {order['phone']}\n"
        order_text += f"📍 {order['address']}\n"
        order_text += f"💳 {payment_text.get(order['payment_type'], order['payment_type'])}\n"
        order_text += f"📊 {status_text.get(order['status'], order['status'])}\n"
        order_text += f"💰 {get_text('payment_status', lang)}: "
        order_text += f"{'✅ ' + get_text('paid', lang) if order['is_paid'] else '⏳ ' + get_text('not_paid', lang)}\n"
        order_text += f"📅 {order['created_at']}\n\n"

        order_text += "📦 Mahsulotlar:\n"
        for idx, item in enumerate(order['items'], 1):
            order_text += f"{idx}. {item['name']} x {item['quantity']}\n"
            order_text += f"   {item['price']:,.0f} so'm\n"

        order_text += f"\n💵 Jami: {order['total']:,.0f} so'm"

        await callback.message.edit_text(
            order_text,
            reply_markup=get_order_detail_keyboard(order_id, order['status'], lang)
        )
    else:
        await callback.answer(get_text('status_update_error', lang), show_alert=True)


@admin_panel_router.callback_query(F.data == "back_to_admin")
@admin_only
async def back_to_admin_menu(callback: CallbackQuery):
    """
    Admin menyuga qaytish
    """
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'uz')

    await callback.message.edit_text(
        get_text('admin_welcome', lang),
        reply_markup=get_admin_menu_keyboard(lang)
    )
    await callback.answer()