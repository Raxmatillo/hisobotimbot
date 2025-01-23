import os
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards import continue_or_no, panel
from loader import db, dp, bot
from os_funkctions import delete_files_with_prefix, get_with_prefix, get_with_prefix_collages
from hisobot import generate_monthly_report
from collage import create_telegram_collage

DOWNLOAD_FOLDER = "downloads/"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@dp.message_handler(text="📝 Hisobot yozish")
async def make_doc(message: types.Message, state: FSMContext):
    db.delete_user_documents(telegram_id=message.from_user.id)
    await message.answer("Hisobot oyligini yozing, oy nomi:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state("month")

@dp.message_handler(state="month", content_types='text')
async def req_title(message: types.Message, state: FSMContext):
    await state.update_data(month=message.text.title())
    await message.answer("Sarlavha yozing (maksimal 60 ta belgi)")
    await state.set_state("title")

@dp.message_handler(state="title", content_types="text")
async def req_descr(message: types.Message, state: FSMContext):
    if len(message.text)>60:
        await message.answer("Sarlavga belgilari 60 tadan oshib ketdi\nIltimos, maksimal 60 belgili matn yuboring")
        return
    else:
        await state.update_data(title=message.text)
        await message.answer("Sarlavha uchun matn yozing (maksimal 300 belgi)")
        await state.set_state("descr")

@dp.message_handler(state="descr", content_types='text')
async def req_photos(message: types.Message, state: FSMContext):
    if len(message.text)>300:
        await message.answer("Matn belgilari 300 tadan oshib ketdi\nIltimos, maksimal 300 belgili matn yuboring")
        return
    else:
        await state.update_data(descr=message.text)
        data = await state.get_data()
        title = data["title"]
        await message.answer(f"<b>{title}</b> bo'yicha rasmlarni albom qilib yuboring (maksimal 5ta rasm)")
        await state.set_state("images")

@dp.message_handler(state="images", content_types='photo')
async def handle_photo(message: types.Message, state: FSMContext):
    try:
        photos = message.photo
        file_info = await bot.get_file(photos[-1].file_id)
        file_path = file_info.file_path
        file_name = f"{DOWNLOAD_FOLDER}{message.from_user.id}_{message.message_id}.jpg"
        
        # Faylni yuklab olish va saqlash
        await bot.download_file(file_path, file_name)
        
        await message.reply(f"Rasm qabul qilindi ✅\n\nDavom etamizmi?", reply_markup=continue_or_no)
        await state.set_state("is_continue")

    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await message.reply("Rasmni saqlashda xatolik yuz berdi.")




@dp.message_handler(state="is_continue", text="Davom etamiz 🔄")
async def to_continue(message: types.Message, state: FSMContext):
    photo_path = get_with_prefix(prefix=str(message.from_user.id))
    photo_name = f"{message.from_user.id}_{message.message_id}.jpg"
    # await state.update_data(image=photo_name)
    create_telegram_collage(images=photo_path, output_path=photo_name)
    delete_files_with_prefix(photo_path)
    
    data = await state.get_data()
    title = data["title"]
    descr = data["descr"]
    month = data["month"]

    db.add_document(
        telegram_id=message.from_user.id,
        title=title,
        text=descr,
        images=photo_name,
        month=month
    )
    
    await message.answer("Sarlavha yozing", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state("title")



@dp.message_handler(state="is_continue", text="Yakunlash 💾")
async def over_(message: types.Message, state: FSMContext):
    xabar = await message.answer("Yozilmoqda, iltimos kutib turing...")
    photo_path = get_with_prefix(prefix=str(message.from_user.id))
    
    photo_name = f"{message.from_user.id}_{message.message_id}.jpg"
    photo_name = f"{message.from_user.id}_{345}.jpg"
    # await state.update_data(image=photo_name)
    
    create_telegram_collage(images=photo_path, output_path=photo_name)
    delete_files_with_prefix(photo_path)
    
    data = await state.get_data()
    title = data["title"]
    descr = data["descr"]
    month = data["month"]

    await state.finish()
    db.add_document(
        telegram_id=message.from_user.id,
        title=title,
        text=descr,
        images=photo_name,
        month=month
    )
    # os.remove(photo_name)
    documents = db.select_document(telegram_id=message.from_user.id)
    
    user = db.select_user(telegram_id=message.from_user.id)
    region = user[2]
    district = user[3]
    school_number = user[4]
    teacher = user[5]
    position = user[6]
    director = user[7]
    year = user[8]

    activities = []
    for document in documents:
        data = {}
        data["title"] = document[2]
        data["description"] = document[3]
        data["image"] = document[4]
        activities.append(data)
    print(f"{activities=}")
    generate_monthly_report(
        region=region,
        district=district,
        school_number=school_number,
        teacher_name=teacher,
        position=position,
        director_name=director,
        month=month,
        year=year,
        activities=activities
    )

    await xabar.delete()
    doc_name = f"@hisobotimbot-{teacher}_{month}.docx"
    await message.answer_document(document=types.InputFile(doc_name), caption="@hisobotimbot", reply_markup=panel)

    photo_path = get_with_prefix_collages(prefix=str(message.from_user.id))
    delete_files_with_prefix(photo_path)
    db.delete_user_documents(telegram_id=message.from_user.id)
    os.remove(doc_name)


@dp.message_handler(state="images", content_types='text')
async def unknown(message: types.Message):
    await message.answer("Iltimos, faqat rasm yuboring (maksimal 5 ta)")