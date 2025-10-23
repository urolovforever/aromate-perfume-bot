# utils/localization.py
"""
Ikki tilli matnlar (O'zbekcha va Ruscha)
"""

TEXTS = {
    # Asosiy matnlar
    'welcome': {
        'uz': "👋 Assalomu aleykum, {name}!\n\nAtir botimizga xush kelibsiz. Quyidagi menyudan kerakli bo'limni tanlang:",
        'ru': "👋 Здравствуйте, {name}!\n\nДобро пожаловать в наш бот парфюмерии. Выберите нужный раздел из меню ниже:"
    },
    'language_selected': {
        'uz': "✅ Til tanlandi: O'zbekcha",
        'ru': "✅ Язык выбран: Русский"
    },
    'main_menu': {
        'uz': "📋 Asosiy menyu",
        'ru': "📋 Главное меню"
    },

    # Menyu tugmalari
    'menu_men': {
        'uz': "👨 Erkaklar atirlari",
        'ru': "👨 Мужские духи"
    },
    'menu_women': {
        'uz': "👩 Ayollar atirlari",
        'ru': "👩 Женские духи"
    },
    'menu_unisex': {
        'uz': "👥 Uniseks atirlar",
        'ru': "👥 Унисекс духи"
    },
    'menu_cart': {
        'uz': "🛒 Savat",
        'ru': "🛒 Корзина"
    },
    'menu_about': {
        'uz': "ℹ️ Biz haqimizda",
        'ru': "ℹ️ О нас"
    },
    'menu_settings': {
        'uz': "⚙️ Sozlamalar",
        'ru': "⚙️ Настройки"
    },

    # Mahsulotlar
    'select_product': {
        'uz': "🎁 Mahsulotni tanlang:",
        'ru': "🎁 Выберите товар:"
    },
    'no_products': {
        'uz': "😔 Hozircha bu kategoriyada mahsulotlar yo'q",
        'ru': "😔 Пока нет товаров в этой категории"
    },
    'product_detail': {
        'uz': "🎁 {name}\n\n📝 {description}\n\n💰 Narxi: {price} so'm",
        'ru': "🎁 {name}\n\n📝 {description}\n\n💰 Цена: {price} сум"
    },
    'product_not_found': {
        'uz': "❌ Mahsulot topilmadi",
        'ru': "❌ Товар не найден"
    },

    # Savat
    'cart_title': {
        'uz': "🛒 Sizning savatingiz:",
        'ru': "🛒 Ваша корзина:"
    },
    'cart_empty': {
        'uz': "😔 Savatingiz bo'sh",
        'ru': "😔 Ваша корзина пуста"
    },
    'added_to_cart': {
        'uz': "✅ Mahsulot savatga qo'shildi!",
        'ru': "✅ Товар добавлен в корзину!"
    },
    'removed_from_cart': {
        'uz': "🗑 Mahsulot savatdan o'chirildi",
        'ru': "🗑 Товар удален из корзины"
    },
    'cart_cleared': {
        'uz': "🗑 Savat tozalandi",
        'ru': "🗑 Корзина очищена"
    },
    'cart_error': {
        'uz': "❌ Xatolik yuz berdi",
        'ru': "❌ Произошла ошибка"
    },
    'total': {
        'uz': "Jami",
        'ru': "Итого"
    },
    'sum': {
        'uz': "so'm",
        'ru': "сум"
    },

    # Buyurtma berish
    'send_phone': {
        'uz': "📞 Telefon raqamingizni yuboring",
        'ru': "📞 Отправьте ваш номер телефона"
    },

    'send_contact': {
        'uz': "📱 Telefon raqamni yuborish",
        'ru': "📱 Отправить номер телефона"
    },
    'send_address': {
        'uz': "📍 Yetkazish manzilini kiriting:",
        'ru': "📍 Введите адрес доставки:"
    },
    'select_payment': {
        'uz': "💳 To'lov turini tanlang:",
        'ru': "💳 Выберите способ оплаты:"
    },
    'payment_cash': {
        'uz': "💵 Naqd pul",
        'ru': "💵 Наличные"
    },
    'order_created': {
        'uz': "✅ Buyurtma #{order_id} qabul qilindi!\n\n💰 Jami: {total} so'm\n\nTez orada siz bilan bog'lanamiz.",
        'ru': "✅ Заказ #{order_id} принят!\n\n💰 Итого: {total} сум\n\nМы свяжемся с вами в ближайшее время."
    },
    'order_error': {
        'uz': "❌ Buyurtma yaratishda xatolik",
        'ru': "❌ Ошибка при создании заказа"
    },

    # Tugmalar
    'add_to_cart': {
        'uz': "🛒 Savatga qo'shish",
        'ru': "🛒 Добавить в корзину"
    },
    'checkout': {
        'uz': "✅ Buyurtma berish",
        'ru': "✅ Оформить заказ"
    },
    'clear_cart': {
        'uz': "🗑 Savatni tozalash",
        'ru': "🗑 Очистить корзину"
    },
    'back': {
        'uz': "⬅️ Orqaga",
        'ru': "⬅️ Назад"
    },
    'back_to_menu': {
        'uz': "🏠 Asosiy menyu",
        'ru': "🏠 Главное меню"
    },
    'previous': {
        'uz': "Oldingi",
        'ru': "Предыдущая"
    },
    'next': {
        'uz': "Keyingi",
        'ru': "Следующая"
    },
    'confirm': {
        'uz': "✅ Tasdiqlash",
        'ru': "✅ Подтвердить"
    },
    'cancel': {
        'uz': "❌ Bekor qilish",
        'ru': "❌ Отменить"
    },

    # Sozlamalar
    'settings_menu': {
        'uz': "⚙️ Sozlamalar",
        'ru': "⚙️ Настройки"
    },
    'change_language': {
        'uz': "🌐 Tilni o'zgartirish",
        'ru': "🌐 Изменить язык"
    },

    # Biz haqimizda
    'about_us': {
        'uz': "ℹ️ Biz haqimizda\n\nBiz original va sifatli atirlarni taklif qilamiz. Barcha mahsulotlar sertifikatlangan.",
        'ru': "ℹ️ О нас\n\nМы предлагаем оригинальную и качественную парфюмерию. Все товары сертифицированы."
    },
    'contact_info': {
        'uz': "📞 Aloqa:\nTelefon: +998 90 123 45 67\nManzil: Toshkent sh.",
        'ru': "📞 Контакты:\nТелефон: +998 90 123 45 67\nАдрес: г. Ташкент"
    },

    # Admin panel
    'admin_welcome': {
        'uz': "👨‍💼 Admin panel\n\nQuyidagi amallardan birini tanlang:",
        'ru': "👨‍💼 Админ панель\n\nВыберите одно из действий:"
    },
    'admin_add_product': {
        'uz': "➕ Yangi atir qo'shish",
        'ru': "➕ Добавить новый парфюм"
    },
    'admin_products_list': {
        'uz': "🗃️ Mahsulotlar ro'yxati",
        'ru': "🗃️ Список товаров"
    },
    'admin_orders_list': {
        'uz': "📦 Buyurtmalar ro'yxati",
        'ru': "📦 Список заказов"
    },
    'admin_statistics': {
        'uz': "📊 Statistika",
        'ru': "📊 Статистика"
    },

    # Mahsulot qo'shish
    'enter_product_name_uz': {
        'uz': "📝 Atir nomini kiriting (O'zbekcha):",
        'ru': "📝 Введите название парфюма (на узбекском):"
    },
    'enter_product_name_ru': {
        'uz': "📝 Atir nomini kiriting (Ruscha):",
        'ru': "📝 Введите название парфюма (на русском):"
    },
    'enter_description_uz': {
        'uz': "📄 Tavsifni kiriting (O'zbekcha):",
        'ru': "📄 Введите описание (на узбекском):"
    },
    'enter_description_ru': {
        'uz': "📄 Tavsifni kiriting (Ruscha):",
        'ru': "📄 Введите описание (на русском):"
    },
    'enter_price': {
        'uz': "💰 Narxni kiriting (so'mda):",
        'ru': "💰 Введите цену (в сумах):"
    },
    'select_category': {
        'uz': "📂 Kategoriyani tanlang:",
        'ru': "📂 Выберите категорию:"
    },
    'send_product_image': {
        'uz': "🖼 Mahsulot rasmini yuboring:",
        'ru': "🖼 Отправьте фото товара:"
    },
    'product_preview': {
        'uz': "👁 Mahsulot ko'rinishi:",
        'ru': "👁 Предпросмотр товара:"
    },
    'product_added': {
        'uz': "✅ Mahsulot muvaffaqiyatli qo'shildi!",
        'ru': "✅ Товар успешно добавлен!"
    },
    'product_cancelled': {
        'uz': "❌ Mahsulot qo'shish bekor qilindi",
        'ru': "❌ Добавление товара отменено"
    },
    'product_add_error': {
        'uz': "❌ Mahsulot qo'shishda xatolik",
        'ru': "❌ Ошибка при добавлении товара"
    },
    'name_too_short': {
        'uz': "❌ Nom juda qisqa (kamida 3 ta belgi)",
        'ru': "❌ Название слишком короткое (минимум 3 символа)"
    },
    'description_too_short': {
        'uz': "❌ Tavsif juda qisqa (kamida 10 ta belgi)",
        'ru': "❌ Описание слишком короткое (минимум 10 символов)"
    },
    'description_too_long': {
        'uz': "❌ Tavsif juda uzun (maksimal 500 belgi)",
        'ru': "❌ Описание слишком длинное (максимум 500 символов)"
    },
    'invalid_price': {
        'uz': "❌ Noto'g'ri narx. Faqat raqam kiriting.",
        'ru': "❌ Неверная цена. Введите только число."
    },
    'invalid_image': {
        'uz': "❌ Noto'g'ri fayl. Iltimos, rasm yuboring.",
        'ru': "❌ Неверный файл. Пожалуйста, отправьте изображение."
    },

    # Kategoriyalar
    'category_men': {
        'uz': "👨 Erkaklar",
        'ru': "👨 Мужские"
    },
    'category_women': {
        'uz': "👩 Ayollar",
        'ru': "👩 Женские"
    },
    'category_unisex': {
        'uz': "👥 Uniseks",
        'ru': "👥 Унисекс"
    },

    # Mahsulotlar ro'yxati
    'products_list_title': {
        'uz': "🗃️ Mahsulotlar ro'yxati:",
        'ru': "🗃️ Список товаров:"
    },
    'product_deleted': {
        'uz': "✅ Mahsulot o'chirildi",
        'ru': "✅ Товар удален"
    },
    'delete_error': {
        'uz': "❌ O'chirishda xatolik",
        'ru': "❌ Ошибка при удалении"
    },

    # Buyurtmalar
    'orders_list_title': {
        'uz': "📦 Buyurtmalar ro'yxati:",
        'ru': "📦 Список заказов:"
    },
    'no_orders': {
        'uz': "📭 Buyurtmalar yo'q",
        'ru': "📭 Нет заказов"
    },
    'order_not_found': {
        'uz': "❌ Buyurtma topilmadi",
        'ru': "❌ Заказ не найден"
    },
    'status_updated': {
        'uz': "✅ Status yangilandi",
        'ru': "✅ Статус обновлен"
    },
    'status_update_error': {
        'uz': "❌ Status yangilashda xatolik",
        'ru': "❌ Ошибка при обновлении статуса"
    },

    # Buyurtma statuslari
    'status_new': {
        'uz': "🆕 Yangi",
        'ru': "🆕 Новый"
    },
    'status_processing': {
        'uz': "⏳ Jarayonda",
        'ru': "⏳ В обработке"
    },
    'status_delivering': {
        'uz': "🚚 Yetkazilmoqda",
        'ru': "🚚 Доставляется"
    },
    'status_completed': {
        'uz': "✅ Yakunlandi",
        'ru': "✅ Завершен"
    },
    'status_cancelled': {
        'uz': "❌ Bekor qilindi",
        'ru': "❌ Отменен"
    },

    # To'lov
    'payment_status': {
        'uz': "To'lov holati",
        'ru': "Статус оплаты"
    },
    'paid': {
        'uz': "To'landi",
        'ru': "Оплачено"
    },
    'not_paid': {
        'uz': "To'lanmagan",
        'ru': "Не оплачено"
    },

    # Buyurtmalar filtri
    'select_order_filter': {
        'uz': "🔍 Buyurtmalarni filtrlash:\n\nQaysi buyurtmalarni ko'rmoqchisiz?",
        'ru': "🔍 Фильтр заказов:\n\nКакие заказы вы хотите увидеть?"
    },
    'filter_all': {
        'uz': "📦 Barcha buyurtmalar",
        'ru': "📦 Все заказы"
    },
    'filter_new': {
        'uz': "🆕 Yangi",
        'ru': "🆕 Новые"
    },
    'filter_processing': {
        'uz': "⏳ Jarayonda",
        'ru': "⏳ В обработке"
    },
    'filter_delivering': {
        'uz': "🚚 Yetkazilmoqda",
        'ru': "🚚 Доставляется"
    },
    'filter_completed': {
        'uz': "✅ Yakunlangan",
        'ru': "✅ Завершенные"
    },
    'filter_today': {
        'uz': "📅 Bugun",
        'ru': "📅 Сегодня"
    },
    'filter_week': {
        'uz': "📅 Haftalik",
        'ru': "📅 За неделю"
    },
    'change_filter': {
        'uz': "🔄 Filtrni o'zgartirish",
        'ru': "🔄 Изменить фильтр"
    },

    # Statistika
    'statistics_title': {
        'uz': "📊 Statistika",
        'ru': "📊 Статистика"
    },
    'select_statistics_period': {
        'uz': "📅 Qaysi davr uchun statistikani ko'rmoqchisiz?",
        'ru': "📅 За какой период вы хотите посмотреть статистику?"
    },
    'filter_month': {
        'uz': "📅 Oylik",
        'ru': "📅 За месяц"
    },
    'top_operators': {
        'uz': "Top operatorlar",
        'ru': "Топ операторы"
    },
    'total_users': {
        'uz': "Foydalanuvchilar",
        'ru': "Пользователи"
    },
    'total_products': {
        'uz': "Mahsulotlar",
        'ru': "Товары"
    },
    'total_orders': {
        'uz': "Buyurtmalar",
        'ru': "Заказы"
    },
    'completed_orders': {
        'uz': "Yakunlangan",
        'ru': "Завершенные"
    },
    'pending_orders': {
        'uz': "Kutilmoqda",
        'ru': "Ожидающие"
    },
    'total_revenue': {
        'uz': "Umumiy daromad",
        'ru': "Общий доход"
    }
}


def get_text(key: str, lang: str = 'uz') -> str:
    """
    Til bo'yicha matnni olish
    """
    return TEXTS.get(key, {}).get(lang, key)