from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import db, dp
from keyboards import yes_or_no, register, cancel, panel


@dp.message_handler(state="*", text="🔙 Bekor qilish")
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Amaliyot bekor qilindi\nBosh menyu uchun /start bosing", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(text="Ro'yxatdan o'tish 👤")
async def request_region(message: types.Message, state: FSMContext):
    await message.answer("Maktab joylashgan viloyatni yozing", reply_markup=cancel)
    await state.set_state("region")

@dp.message_handler(state="region", content_types='text')
async def request_district(message: types.Message, state: FSMContext):
    await state.update_data(region=message.text)
    await message.answer("Hududingizni tuman/shahar nomi bilan kiriting\nMasalan: Shahrixon tumani, Farg'ona shahri")
    await state.set_state("district")

@dp.message_handler(state="district", content_types='text')
async def request_school_number(message: types.Message, state: FSMContext):
    await state.update_data(district=message.text)
    await message.answer("Maktab yoki DIMIni quyidagicha kiriting\n<i>56-maktab, 26-DIMI</i>")
    await state.set_state("school_number")

@dp.message_handler(state="school_number", content_types='text')
async def request_teacher(message: types.Message, state: FSMContext):
    await state.update_data(school_number=message.text)
    await message.answer("O'qituvchi ism-familyasi")
    await state.set_state("teacher")

@dp.message_handler(state="teacher", content_types='text')
async def request_position(message: types.Message, state: FSMContext):
    await state.update_data(teacher=message.text.title())
    await message.answer("Qanday lavozimda ishlaysiz\nMasalan: amaliyotchi psixologi, informatika o'qituvchisi....")
    await state.set_state("position")

@dp.message_handler(state="position", content_types='text')
async def request_director(message: types.Message, state: FSMContext):
    await state.update_data(position=message.text)
    await message.answer("Maktab direktori ism-familyasi")
    await state.set_state("director")

@dp.message_handler(state="director", content_types='text')
async def request_year(message: types.Message, state: FSMContext):
    await state.update_data(director=message.text.title())
    await message.answer("O'quv yili\nMasalan: 2024-2025")
    await state.set_state("year")

@dp.message_handler(state="year", content_types='text')
async def request_year(message: types.Message, state: FSMContext):
    await state.update_data(year=message.text)
    data = await state.get_data()
    region = data["region"]
    district = data["district"]
    school_number = data["school_number"]
    teacher = data["teacher"]
    position = data["position"]
    director = data["director"]
    year = data["year"]
    text = "<b>Ma'lumotlarni tasdiqlaysizmi</b>\n\n"
    text += f"Viloyat: {region}\n"\
            f"Tuman/shahar: {district}\n"\
            f"Maktab: {school_number}\n"\
            f"O'qituvchi: {teacher}\n"\
            f"Lavozimi: {position}\n"\
            f"Maktab direktori: {director}\n"\
            f"O'quv yili: {year}\n"
    await message.answer(text=text, reply_markup=yes_or_no)
    await state.set_state('verify')

@dp.message_handler(state="verify", text="✅ Tasdiqlayman")
async def verified(message: types.Message, state: FSMContext):
    data = await state.get_data()
    region = data["region"]
    district = data["district"]
    school_number = data["school_number"]
    teacher = data["teacher"]
    position = data["position"]
    director = data["director"]
    year = data["year"]
    try:
        user = db.select_user(telegram_id=message.from_user.id)
        if user:
            db.update_user(
                region=region,
                district=district,
                school_number=school_number,
                teacher_name=teacher,
                position=position,
                director_name=director,
                year=year,
                telegram_id=message.from_user.id
            )
        else:
            db.add_user(
                telegram_id=message.from_user.id,
                region=region,
                district=district,
                school_number=school_number,
                teacher_name=teacher,
                position=position,
                director_name=director,
                year=year
            )
        await message.reply("<b>Ma'lumotlar muvaffaqiyatli saqlandi ✅</b>", reply_markup=panel, parse_mode='html')
    except Exception as err:
        print("Ma'lumot saqlashda xatolik", err)
    await state.finish()

@dp.message_handler(state="verify", text="❌ Tasdiqlamayman")
async def unverify(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Boshqatdan ro'yxatdan o'tishingiz mumkin", reply_markup=register)