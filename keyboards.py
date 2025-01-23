from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

register = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ro'yxatdan o'tish")
        ]
    ], resize_keyboard=True
)


yes_or_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("✅ Tasdiqlayman"),
            KeyboardButton("❌ Tasdiqlamayman")
        ]
    ], resize_keyboard=True
)

cancel = ReplyKeyboardMarkup(
    keyboard=[
            [KeyboardButton(text="🔙 Bekor qilish")]
    ], resize_keyboard=True
)

panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("📝 Hisobot yozish"),
            KeyboardButton("ℹ️ Ma'lumotlarim"),
        ],
        [
            KeyboardButton("🔄 Ma'lumotlarimni yangilash")
        ]
    ], resize_keyboard=True
)

continue_or_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Davom etamiz 🔄"),
            KeyboardButton("Yakunlash 💾")
        ]
    ], resize_keyboard=True
)