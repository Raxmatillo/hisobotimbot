from aiogram import types
from aiogram.utils import executor
from keyboards import register, panel
import register_user
import make_document
from loader import dp, db

from os_funkctions import get_with_prefix

# photo_path = get_with_prefix(prefix=str(5590726880))


# d = db.select_document(telegram_id=5590726880)
# print(d)

# Start komandasi uchun handler
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user = db.select_user(telegram_id=message.from_user.id)
    if user:
        await message.answer("Siz asosiy oynadasiz 😊", reply_markup=panel)
    else:
        await message.answer("Assalomu alaykum!\n\nBotdan to'liq foydalanish uchun ro'yxatdan o'tishingiz kerak!", reply_markup=register)

# from aiogram.dispatcher import FSMContext
# from keyboards import cancel
# @dp.message_handler(text="Ro'yxatdan o'tish")
# async def request_region(message: types.Message, state: FSMContext):
#     await message.answer("Maktab joylashgan viloyatni yozing", reply_markup=cancel)
#     await state.set_state("region")

@dp.message_handler(text="ℹ️ Ma'lumotlarim")
async def myProfile(message: types.Message):
    user = db.select_user(telegram_id=message.from_user.id)
    region = user[2]
    district = user[3]
    school_number = user[4]
    teacher = user[5]
    position = user[6]
    director = user[7]
    year = user[8]
    text = "<b>Ma'lumotlarim</b>\n\n"
    text += f"Viloyat: {region}\n"\
            f"Tuman/shahar: {district}\n"\
            f"Maktab: {school_number}-maktab\n"\
            f"O'qituvchi: {teacher}\n"\
            f"Lavozimi: {position}\n"\
            f"Maktab direktori: {director}\n"\
            f"O'quv yili: {year}\n"
    await message.answer(text=text)

@dp.message_handler(text="🔄 Ma'lumotlarimni yangilash")
async def update_mydata(message: types.Message):
    await message.answer("Ma'lumotlarni yangilash uchun qayta ro'yxatdan o'tishingiz kerak.\nAgar rostan ham yangilamoqchi bo'lsangiz quyidagi tugmani bosing!\n\nBosh menyu uchun /start", reply_markup=register)

# Botni ishga tushirish
if __name__ == '__main__':
    print("Bot ishga tushirildi...")
    db.create_table_users()
    # db.delete_documents()
    db.create_table_documents()
    executor.start_polling(dp, skip_updates=True)
