# 🌸 Atir Sotish Telegram Boti

Telegram orqali erkaklar, ayollar va uniseks atirlarini sotish uchun ikki tilli (O'zbekcha/Ruscha) bot.

## 📋 Xususiyatlari

### 👥 Foydalanuvchilar uchun:
- 🌐 Ikki tilli interfeys (O'zbekcha / Ruscha)
- 👨👩👥 3 ta kategoriya: Erkaklar, Ayollar, Uniseks
- 🛒 Savat funksiyasi
- 📦 Mahsulot tafsilotlari (rasm, nom, tavsif, narx)
- 💳 3 xil to'lov turi: Naqd, Click, Payme
- 📱 Telefon raqami va manzil kiritish
- ℹ️ Biz haqimizda va Aloqa ma'lumotlari
- ⚙️ Sozlamalar (tilni o'zgartirish)

### 👨‍💼 Adminlar uchun:
- ➕ Yangi mahsulot qo'shish
- 🗃️ Mahsulotlar ro'yxati va o'chirish
- 📦 Buyurtmalar boshqaruvi
- 📊 Statistika
- 🔄 Buyurtma statusini o'zgartirish

## 🚀 O'rnatish

### 1. Repozitoriyani klonlash
```bash
git clone https://github.com/your-username/atir-bot.git
cd atir-bot
```

### 2. Virtual muhit yaratish
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 3. Kerakli kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. .env faylini sozlash
`.env` faylini yarating va quyidagi ma'lumotlarni kiriting:

```env
BOT_TOKEN=your_bot_token_from_botfather
DATABASE_URL=sqlite:///atir_bot.db
ADMIN_IDS=your_telegram_id,another_admin_id
```

### 5. Botni ishga tushirish
```bash
python bot.py
```

## 📁 Loyiha Tuzilishi

```
atir-bot/
├── bot.py                       # Asosiy ishga tushiruvchi fayl
├── config.py                    # Konfiguratsiya
├── requirements.txt             # Kutubxonalar
├── .env                         # Yashirin ma'lumotlar
├── README.md                    # Loyiha haqida
│
├── handlers/                    # Barcha handlerlar
│   ├── __init__.py
│   ├── user/                    # Foydalanuvchi handlerlari
│   │   ├── __init__.py
│   │   ├── start.py             # /start va til tanlash
│   │   ├── menu.py              # Kategoriyalar menyusi
│   │   ├── product.py           # Mahsulot ko'rish
│   │   └── cart.py              # Savat va buyurtma
│   │
│   └── admin/                   # Admin handlerlari
│       ├── __init__.py
│       ├── panel.py             # Admin panel
│       └── add_product.py       # Mahsulot qo'shish
│
├── database/                    # Ma'lumotlar bazasi
│   ├── __init__.py
│   ├── models.py                # ORM modellar
│   └── db.py                    # Database funksiyalari
│
├── keyboards/                   # Tugmalar
│   ├── __init__.py
│   ├── user_keyboards.py        # Foydalanuvchi tugmalari
│   └── admin_keyboards.py       # Admin tugmalari
│
└── utils/                       # Yordamchi funksiyalar
    ├── __init__.py
    ├── localization.py          # Tarjimalar
    ├── decorators.py            # Decoratorlar
    └── validators.py            # Validatorlar
```

## 🔧 Admin Bo'lish

1. Telegram ID ni aniqlash: [@userinfobot](https://t.me/userinfobot)
2. `.env` faylidagi `ADMIN_IDS` ga qo'shish
3. Botni qayta ishga tushirish
4. `/admin` komandasini yuborish

## 💳 To'lov Tizimlarini Ulash

### Click
1. Click merchant akkaunt ochish
2. `.env` fayliga ma'lumotlarni kiriting:
```env
CLICK_MERCHANT_ID=your_merchant_id
CLICK_SERVICE_ID=your_service_id
CLICK_SECRET_KEY=your_secret_key
```

### Payme
1. Payme merchant akkaunt ochish
2. `.env` fayliga ma'lumotlarni kiriting:
```env
PAYME_MERCHANT_ID=your_merchant_id
PAYME_SECRET_KEY=your_secret_key
```

## 📊 Database

Loyiha SQLite ishlatadi (production uchun PostgreSQL tavsiya etiladi).

PostgreSQL ga o'tish uchun:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/atir_bot
```

## 🐛 Muammolarni Hal Qilish

### Bot ishlamayapti
- `.env` fayli to'g'ri sozlanganligini tekshiring
- Bot tokenini tekshiring
- Internet aloqani tekshiring

### Database xatoligi
- `atir_bot.db` faylini o'chirib, qayta ishga tushiring

### Admin panel ishlamayapti
- Telegram ID to'g'ri kiritilganligini tekshiring
- Vergul bilan ajratilganligini tekshiring

## 📝 License

MIT License

## 👨‍💻 Muallif

Urolov Nizomjon

## 🤝 Hissa Qo'shish

Pull requestlar qabul qilinadi!

## 📞 Aloqa

- Email: nizomjonurolov.com

---

⭐️ Agar loyiha foydali bo'lsa, GitHub'da yulduzcha qoldiring!