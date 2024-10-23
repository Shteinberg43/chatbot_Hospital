from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from keyboards_messages import messages as msg
from keyboards_messages import keyboards as kb
from database.db import create_db
from filters.callback_data import AdminInterfaceCallback, AdminBackCallback
from filters.states import AdminStates

admin_r = Router()
db = create_db()


@admin_r.message(F.text == "/admin")
async def admin_start(message: Message, state: FSMContext):
	await message.answer(text=msg.ADMIN_START + msg.ADMIN_FUNCTION, parse_mode='HTML',
	                     reply_markup=kb.get_admin_interface().as_markup())
	await state.set_state(AdminStates.menu)

#списки
@admin_r.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_list_departments == True))
async def list_departments(query: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(chat_id=query.from_user.id, text=msg.get_names(db.get_departments()))
    await bot.send_message(chat_id=query.from_user.id, text=('Список отедлов был успешно предоставлен! \n'
                                                             'вернуться в меню - /admin \nвыбрать новую роль - /start'))
    await state.clear()


@admin_r.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_list_doctors == True))
async def list_doctors(query: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(chat_id=query.from_user.id, text=msg.get_names(db.get_doctors()))
    await bot.send_message(chat_id=query.from_user.id, text=('Список врачей был успешно предоставлен! \n'
                                                             'вернуться в меню - /admin \nвыбрать новую роль - /start'))
    await state.clear()

#отчёты
@admin_r.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_report == True))
async def list_departments(query: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(chat_id=query.from_user.id, text="Выберите отчёт!",
                           reply_markup=kb.get_admin_report().as_markup())
#чьи пациенты умирают
@admin_r.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_doctor_killed == True))
async def list_doctors(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text=msg.get_names(db.get_doctors_killed()))
	await bot.send_message(chat_id=query.from_user.id, text=('\nвернуться в меню - /admin \nвыбрать новую роль - /start'))
	await state.clear()
#лучшие
@admin_r.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_great_doctor == True))
async def list_doctors(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text=msg.get_names(db.get_doctors_great_in_depart()))
	await bot.send_message(chat_id=query.from_user.id,
	                       text=('\nвернуться в меню - /admin \nвыбрать новую роль - /start'))
	await state.clear()

#частота
@admin_r.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_frequency == True))
async def begin(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id,
	                       text=("Введите начальную и конечную даты через запятую в формате yyyy-mm-dd"))
	await state.set_state(AdminStates.frequency)


@admin_r.message(AdminStates.frequency)
async def date(message: Message, state: FSMContext):
	date = list(message.text.split(", "))
	await message.answer(text=msg.get_names(db.get_frequency_diag(date[0],date[1])))
	await message.answer(text=('\nвернуться в меню - /admin \nвыбрать новую роль - /start'))
	await state.clear()


#история
@admin_r.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_all_history == True))
async def begin(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id,
	                       text=("Введите год в формате <b>гггг</b>, \nесли хотите получить отчёт за конкретный год,"
	                             "или напишите <b>весь период</b>, \nесли хотите получить отчёт"
	                             " за весь период работы больницы"), parse_mode='HTML')
	await state.set_state(AdminStates.history)


@admin_r.message(AdminStates.history)
async def date(message: Message, state: FSMContext):
	if message.text == "весь период":
		await message.answer(text="Обозначения: \n1 - отделение.\n2 - количество поступлений.\n3 - количество вылеченных пациентов.\n"
		                          "4 - количество погибших.\n5 - количество погибших в другом отделении.\nТаблица:\n"
		                          "        1\n        2        3        4        5"
		                          + msg.get_names(db.get_history()))
		await message.answer(text=('\nвернуться в меню - /admin \nвыбрать новую роль - /start'))
		await state.clear()
	else:
		date = list(message.text.split(", "))
		await message.answer(text="Обозначения: \n1 - отделение.\n2 - количество поступлений.\n3 - количество вылеченных пациентов.\n"
		                          "4 - количество погибших.\n5 - количество погибших в другом отделении.\nТаблица:\n"
		                          "        1\n        2        3        4        5"
		                          + msg.get_names(db.get_history_year(date[0])))
		await message.answer(text=('\nвернуться в меню - /admin \nвыбрать новую роль - /start'))
		await state.clear()



#создание отделения
@admin_r.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_create_department == True))
async def create_department(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text="Введите название отдела:")
	await state.set_state(AdminStates.department_name)


@admin_r.message(AdminStates.department_name)
async def department_name(message: Message, state: FSMContext):
	if db.is_depart_exist(message.text):
		await state.update_data(title=message.text)
		await message.answer(text="Введите кол-во коек в отделении")
		await state.set_state(AdminStates.department_create)
	else:
		await message.answer(text="Отдел с таким названием уже есть в больнице.")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_admin().as_markup())
		await state.set_state(AdminStates.back)


@admin_r.message(AdminStates.department_create)
async def department_beds(message: Message, state: FSMContext):
	await state.update_data(beds=int(message.text))
	info = await state.get_data()
	db.create_department(info["title"], info["beds"])
	await message.answer(text="Отдел был успешно создан! \n"
	                          "вернутьcя в меню - /admin \nвыбрать новую роль - /start")
	await state.set_state(AdminStates.back)


#создание диагноза
@admin_r.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_add_diagnos == True))
async def create_diagnos(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text="Введите название диагноза:")
	await state.set_state(AdminStates.diagnos_add)


@admin_r.message(AdminStates.diagnos_add)
async def diagnos_name(message: Message, state: FSMContext):
	if db.is_diag_exist(message.text):
		await state.update_data(title=message.text)
		await message.answer(text="Введите название отделения, в котором будут лечить этот диагноз\n"
		                          "Список отделений:" + msg.get_names(db.get_departments())
		                          + "\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
		await state.set_state(AdminStates.diagnos_create)
	else:
		await message.answer(text="Диагноз с таким названием уже есть в списке.")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_admin().as_markup())
		await state.set_state(AdminStates.back)

@admin_r.message(AdminStates.diagnos_create)
async def diagnos_create(message: Message, state: FSMContext):
	dep_id = db.get_department_id(message.text)
	await state.update_data(dep_id=dep_id)
	info = await state.get_data()
	db.create_diagnos(info["dep_id"], info["title"])
	await message.answer(text="Диагноз был успешно создан! \n"
	                          "вернутьcя в меню - /admin \nвыбрать новую роль - /start")
	await state.clear()

#создание лекарств
@admin_r.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_add_medicine == True))
async def create_medicine(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text="Введите название лекарства"
	                                                        " и максимальную дневную дозировку через запятую:")
	await state.set_state(AdminStates.medicine_add)


@admin_r.message(AdminStates.medicine_add)
async def medicine_name(message: Message, state: FSMContext):
	medicine = list(message.text.split(", "))
	if db.is_medic_exist(medicine[0]):
		await state.update_data(title=medicine[0])
		await state.update_data(max_dos=int(medicine[1]))
		info = await state.get_data()
		db.create_medicine(info["max_dos"], info["title"])
		await message.answer(text="Лекарство было успешно добавлено! \n"
		                          "вернутьcя в меню - /admin \nвыбрать новую роль - /start")
		await state.clear()
	else:
		await message.answer(text="Лекарство с таким названием уже есть в списке.")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_admin().as_markup())
		await state.set_state(AdminStates.back)

#создание процедур
@admin_r.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_add_procedure == True))
async def create_procedure(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text="Введите название процедуры"
	                                                        " и максимальную дневную дозировку через запятую:")
	await state.set_state(AdminStates.procedure_add)


@admin_r.message(AdminStates.procedure_add)
async def procedure_name(message: Message, state: FSMContext):
	procedure = list(message.text.split(", "))
	if db.is_medic_exist(procedure[0]):
		await state.update_data(title=procedure[0])
		await state.update_data(max_dos=int(procedure[1]))
		info = await state.get_data()
		db.create_procedure(info["max_dos"], info["title"])
		await message.answer(text="Процедура была успешно добавлена! \n"
		                          "вернутьcя в меню - /admin \nвыбрать новую роль - /start")
		await state.clear()
	else:
		await message.answer(text="Процедура с таким названием уже есть в списке.")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_admin().as_markup())
		await state.set_state(AdminStates.back)

#Связка диагноза с процедурами и лекарствами
@admin_r.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_connect_diagnos == True))
async def connect_medic(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text="Введите название процедуры или лекарства:\n"
	                        "Список:" + msg.get_names(db.get_med_proc())
	                        + "\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
	await state.set_state(AdminStates.medicine_connect)

@admin_r.message(AdminStates.medicine_connect)
async def connect_diag(message: Message, state: FSMContext):
	med_id = db.get_med_proc_id(message.text)
	await state.update_data(med_id=med_id)
	await message.answer(text="Введите названия диагнозов через запятую:\n"
	                          "Список:" + msg.get_names(db.get_diagnos())
	                          + "\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
	await state.set_state(AdminStates.connect_add)

@admin_r.message(AdminStates.connect_add)
async def connect_add(message: Message, state: FSMContext):
	diag_arr = list(message.text.split(", "))
	for elem in diag_arr:
		diag_id = db.get_diagnos_id(elem)
		await state.update_data(diag_id=diag_id)
		info = await state.get_data()
		if db.is_med_proc_exist(info["diag_id"], info["med_id"]):
			db.create_connect_diag_med(info["diag_id"], info["med_id"])
	if len(diag_arr)>0:
		await message.answer(text="Связи были успешно добавлены! \n"
	                             "вернутьcя в меню - /admin \nвыбрать новую роль - /start")
		await state.clear()
	else:
		await message.answer(text="Связь была успешно добавлена! \n"
		                          "вернутьcя в меню - /admin \nвыбрать новую роль - /start")
		await state.clear()

#добавление врача
@admin_r.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_add_doctor == True))
async def doctor_name(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text="Введите ФИО (Фамилия И.О.) и профессию через запятую:")
	await state.set_state(AdminStates.doctor_depart)

@admin_r.message(AdminStates.doctor_depart)
async def doctor_depart(message: Message, state: FSMContext):
	doctor = list(message.text.split(", "))
	if db.is_doctor_exist(doctor[0]):
		await state.update_data(name=doctor[0])
		await state.update_data(prof=doctor[1])
		await message.answer(text="Введите название отделения, в котором будет работать врач\n"
		                          "Список отделений:" + msg.get_names(db.get_departments())
		                          + "\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
		await state.set_state(AdminStates.doctor_employ)
	else:
		await message.answer(text="Врач с таким ФИО уже есть в списке.")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_admin().as_markup())
		await state.set_state(AdminStates.back)

@admin_r.message(AdminStates.doctor_employ)
async def doctor_employ(message: Message, state: FSMContext):
	dep_id = db.get_department_id(message.text)
	await state.update_data(dep_id=dep_id)
	info = await state.get_data()
	db.create_doctor(info["dep_id"], info["name"], info["prof"])
	await message.answer(text="Врач был успешно принят! \n"
	                          "вернутьcя в меню - /admin \nвыбрать новую роль - /start")
	await state.clear()

#Уволнение врача
@admin_r.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_delete_doctor == True))
async def doctor_dismiss_name(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text="Введите ФИО врача\n"
		                          "Список врачей:" + msg.get_names(db.get_doctors())
		                          + "\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
	await state.set_state(AdminStates.doctor_delete)

@admin_r.message(AdminStates.doctor_delete)
async def doctor_delete(message: Message, state: FSMContext):
	if db.is_doctor_exist(message.text):
		await message.answer(text="Врача с таким ФИО нет в списке.")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_admin().as_markup())
		await state.set_state(AdminStates.back)
	elif db.is_doctor_have_patient(message.text):
		await message.answer(text="Врача нельзя уволить, так как у него есть пациенты.")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_admin().as_markup())
		await state.set_state(AdminStates.back)
	else:
		db.dismiss_doctor(message.text)
		await message.answer(text="Врач был уволен! \n"
		                          "вернутьcя в меню - /admin \nвыбрать новую роль - /start")
		await state.clear()

#Регистрация пациента
@admin_r.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_add_patient == True))
async def patient_name(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text="Введите ФИО (Фамилия И.О.) пациента, его пол (м/ж) и возраст через запятую:")
	await state.set_state(AdminStates.patient_add)

@admin_r.message(AdminStates.patient_add)
async def patient_add(message: Message, state: FSMContext):
	patient = list(message.text.split(", "))
	if db.is_patient_exist(patient[0]):
		await state.update_data(name=patient[0])
		await state.update_data(gender=patient[1])
		await state.update_data(age=int(patient[2]))
		info = await state.get_data()
		db.create_patient(info["name"], info["gender"], info["age"])
		await message.answer(text="Пациент был успешно зарегистрирован! \n"
		                          "вернутьcя в меню - /admin \nвыбрать новую роль - /start")
		await state.clear()
	else:
		await message.answer(text="Пациент с таким ФИО уже существет!")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_admin().as_markup())
		await state.set_state(AdminStates.back)


@admin_r.callback_query(AdminStates.back, AdminBackCallback.filter(F.is_back == True))
async def backpacking(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id,text=msg.ADMIN,
	                     reply_markup=kb.get_admin_interface().as_markup())
	await state.set_state(AdminStates.menu)

@admin_r.callback_query(AdminStates.back, AdminBackCallback.filter(F.is_back == False))
async def end(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text='Отличная работа! \nвыбрать новую роль - /start')
	await state.clear()
