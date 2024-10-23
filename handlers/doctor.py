from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from keyboards_messages import messages as msg
from keyboards_messages import keyboards as kb
from database.db import create_db
from filters.callback_data import DoctorInterfaceCallback, DoctorBackCallback
from filters.states import DoctorStates
#from datetime import datetime

doctor_r = Router()
db = create_db()

@doctor_r.message(F.text == "/doctor")
async def admin_start(message: Message, state: FSMContext):
	await message.answer(text=msg.DOCTOR_START,
	                     reply_markup=kb.get_doctor_interface().as_markup())
	await state.set_state(DoctorStates.menu)

#оформление пациента
@doctor_r.callback_query(DoctorStates.menu, DoctorInterfaceCallback.filter(F.is_add_patient == True))
async def select_patient(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text="Выберите пациента:\n"
	                                                        "Список:\nФИО        Пол Возраст"
	                                                        + msg.get_names(db.get_patients()) +
	                                                        "\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
	await state.set_state(DoctorStates.add_patient)

@doctor_r.message(DoctorStates.add_patient)
async def add_patient(message: Message, state: FSMContext):
	patient_id = db.get_patient_id(message.text)
	if db.is_entrance_exist(patient_id):
		await message.answer(text="Пожалуйста, запишите первичные жалобы пациента через запятую.\n")
		await state.update_data(patient_id=patient_id)
		await state.set_state(DoctorStates.patient_depart)
	else:
		await message.answer(text="Пациент с таким ФИО уже оформлен!")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_doctor().as_markup())
		await state.set_state(DoctorStates.back)

@doctor_r.message(DoctorStates.patient_depart)
async def patient_depart(message: Message, state: FSMContext):
	await state.update_data(problem=message.text)
	await message.answer(text="Укажите отделение со свободными койками, в котором он будет проходить лечение!\n"
	                          "Список:\nНазвание      свободных мест\n" + msg.get_names(db.get_departments())
	                          + "\n<b>используйте CTRL+C и CTRL+V.</b>", parse_mode = 'HTML')
	await state.set_state(DoctorStates.add_patient_end)

@doctor_r.message(DoctorStates.add_patient_end)
async def add_patient(message: Message, state: FSMContext):
	depart_id = db.get_department_id(message.text)
	await state.update_data(department=depart_id)
	info = await state.get_data()
	dep_bed = db.get_department_bed(info["department"])
	if dep_bed > 0:
		dep_bed = -1
		db.create_entrance(info["department"], info["patient_id"], info["problem"])
		db.update_department_bed(info["department"], dep_bed)
		await message.answer(text="Пациент был успешно оформлен! \n"
	                             "вернутьcя в меню - /doctor \nвыбрать новую роль - /start")
		await state.clear()
	else:
		await message.answer(text="В этом отделении нет свободных мест!")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_doctor().as_markup())
		await state.set_state(DoctorStates.back)

#назначение диагноза
@doctor_r.callback_query(DoctorStates.menu, DoctorInterfaceCallback.filter(F.is_add_history == True))
async def select_patient(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text="Выберите пациента:\n"
	                                                        "Список:\nФИО        Пол Возраст"
	                                                        + msg.get_names(db.get_patients()) +
	                                                        "\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
	await state.set_state(DoctorStates.select_doctor)

@doctor_r.message(DoctorStates.select_doctor)
async def select_doctor(message: Message, state: FSMContext):
	patient_id = db.get_patient_id(message.text)
	if db.is_entrance_exist(patient_id):
		await message.answer(text="Пациент не оформлен!\n")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_doctor().as_markup())
		await state.set_state(DoctorStates.back)
	else:
		entrance_id = db.get_entrance_id(patient_id)
		await state.update_data(patient_id=patient_id)
		await state.update_data(entrance_id=entrance_id)
		await message.answer(text="Для дальнейшей работы введите своё ФИО:\n"
	                            "Список:" + msg.get_names(db.get_doctors()) +
	                            "\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
		await state.set_state(DoctorStates.add_diag)

@doctor_r.message(DoctorStates.add_diag)
async def add_diagnos(message: Message, state: FSMContext):
	doctor_id = db.get_doctor_id(message.text)
	await state.update_data(doctor_id=doctor_id)
	await message.answer(text="Выберите диагноз:\n"
	                        "Список:" + msg.get_names(db.get_doctors_diagnose(doctor_id)) +
	                        "\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
	await state.set_state(DoctorStates.create_history)

@doctor_r.message(DoctorStates.create_history)
async def create_history(message: Message, state: FSMContext):
	diag_id = db.get_diagnos_id(message.text)
	await state.update_data(diag_id=diag_id)
	info = await state.get_data()
	if db.is_history_exist(info["doctor_id"], info["diag_id"], info["entrance_id"]):
		if db.is_uniq_doctor_for_create(info["doctor_id"], info["entrance_id"]):
			db.update_doctor_active_patient(info["doctor_id"])
		db.create_history(info["doctor_id"], info["diag_id"], info["entrance_id"])
		await message.answer(text="Диагноз был успешно поставлен!\n"
		                          "вернутьcя в меню - /doctor \nвыбрать новую роль - /start")
		await state.clear()
	else:
		await message.answer(text="Этот диагноз уже поставлен, но не вылечен!")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_doctor().as_markup())
		await state.set_state(DoctorStates.back)

#назначение лечения пациенту
@doctor_r.callback_query(DoctorStates.menu, DoctorInterfaceCallback.filter(F.is_add_appointment == True))
async def select_patient(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text="Выберите пациента:\n"
	                                                        "Список:\nФИО        Пол Возраст"
	                                                        + msg.get_names(db.get_patients()) +
	                                                        "\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
	await state.set_state(DoctorStates.patient_name)

@doctor_r.message(DoctorStates.patient_name)
async def patient_name(message: Message, state: FSMContext):
	patient_id = db.get_patient_id(message.text)
	if db.is_entrance_exist(patient_id):
		await message.answer(text="Пациент не оформлен!\n")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_doctor().as_markup())
		await state.set_state(DoctorStates.back)
	else:
		await state.update_data(patient_id=patient_id)
		entrance_id = db.get_entrance_id(patient_id)
		await state.update_data(entrance_id=entrance_id)
		await message.answer(text="Для дальнейшей работы введите своё ФИО:\n"
		                          "Список:" + msg.get_names(db.get_doctors()) +
		                          "\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
		await state.set_state(DoctorStates.select_diag)

@doctor_r.message(DoctorStates.select_diag)
async def select_diag(message: Message, state: FSMContext):
	doctor_id = db.get_doctor_id(message.text)
	await state.update_data(doctor_id=doctor_id)
	info = await state.get_data()
	await message.answer(text="Для назначения лечения выберите один \nиз поставленных Вами диагнозов:\n"
	                          "Список:" +
	                          msg.get_names(db.get_diagnoses_from_history(info["doctor_id"], info["entrance_id"]))
	                          + "\nнет подходящего\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
	await state.set_state(DoctorStates.select_med_proc)

@doctor_r.message(DoctorStates.select_med_proc)
async def select_med_proc(message: Message, state: FSMContext):
	if message.text == "нет подходящего":
		await message.answer(text="Для назначения лечения необходимо поставить диагноз!\n")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_doctor().as_markup())
		await state.set_state(DoctorStates.back)
	else:
		diag_id = db.get_diagnos_id(message.text)
		await state.update_data(diag_id=diag_id)
		info = await state.get_data()
		history_id = db.get_history_id(info["doctor_id"], info["diag_id"], info["entrance_id"])
		await state.update_data(history_id=history_id)
		await message.answer(text="Выберите одно лекарство или процедуру:\n"
		                          "<b>Список лекарств:</b>" + msg.get_names(db.get_specific_med(info["diag_id"])) +
		                          "\n<b>Список процедур:</b>" + msg.get_names(db.get_specific_proc(info["diag_id"])) +
		                          "\nнет подходящего\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
		await state.set_state(DoctorStates.select_dosage)

@doctor_r.message(DoctorStates.select_dosage)
async def select_dosage(message: Message, state: FSMContext):
	if message.text == "нет подходящего":
		await message.answer(text="Нужного препарата нет в больнице или у Вас нет к нему доступа!\n")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_doctor().as_markup())
		await state.set_state(DoctorStates.back)
	else:
		med_proc_id = db.get_med_proc_id(message.text)
		await state.update_data(med_proc_id=med_proc_id)
		info = await state.get_data()
		possible_dosage = db.get_max_possible_dosage(info["entrance_id"], info["med_proc_id"])
		await state.update_data(possible_dosage=possible_dosage)
		if db.is_appointment_exist(info["history_id"], info["med_proc_id"]):#ветвь если нет назначений с таким препаратом
			await message.answer(text="Максимальная возможная доза с учётом других назначений: "
			                          + str(possible_dosage) +
			                          "\nВведите дневную дозировку лекарства/процедуры:")
			await state.set_state(DoctorStates.add_appointment)
		else:
			await message.answer(text="Этот препарат уже назначен, Вы хотите изменить дозировку?\n", 
			                     reply_markup=kb.get_doctor_appointment().as_markup())
			await state.set_state(DoctorStates.change_appointment)

@doctor_r.message(DoctorStates.add_appointment)
async def add_appointment(message: Message, state: FSMContext):
	await state.update_data(dosage=int(message.text))
	info = await state.get_data()
	if info["dosage"] > info["possible_dosage"]:
		await message.answer(text="Превышена максимальная дневная доза! Назначение отменено!\n")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_doctor().as_markup())
		await state.set_state(DoctorStates.back)
	else:
		db.create_appointment(info["history_id"], info["med_proc_id"], info["dosage"])
		await message.answer(text="Препарат был успешно назначен!\n"
		                          "вернутьcя в меню - /doctor \nвыбрать новую роль - /start")
		await state.clear()


@doctor_r.callback_query(DoctorStates.change_appointment, DoctorInterfaceCallback.filter(F.is_change_dosage == True))
async def change_dosage(query: CallbackQuery, state: FSMContext, bot: Bot):
	info = await state.get_data()
	last_appointment = db.get_appointment_id(info["history_id"], info["med_proc_id"])
	is_dosage = db.get_appointment_dosage(last_appointment)
	possible_dosage = info["possible_dosage"] + is_dosage
	await state.update_data(possible_dosage=possible_dosage)
	await state.update_data(last_appointment=last_appointment)
	info = await state.get_data()
	await bot.send_message(chat_id=query.from_user.id, text="Максимальная возможная доза с учётом других назначений: "
			                          + str(info["possible_dosage"]) +
			                          "\nВведите дневную дозировку лекарства/процедуры:")
	await state.set_state(DoctorStates.remake_appointment)

@doctor_r.message(DoctorStates.remake_appointment)
async def remake_appointment(message: Message, state: FSMContext):
	await state.update_data(dosage=int(message.text))
	info = await state.get_data()
	if info["dosage"] > info["possible_dosage"]:
		await message.answer(text="Превышена максимальная дневная доза! Назначение отменено!\n")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_doctor().as_markup())
		await state.set_state(DoctorStates.back)
	else:
		db.close_appointment(info["last_appointment"])
		db.create_appointment(info["history_id"], info["med_proc_id"], info["dosage"])
		await message.answer(text="Дозировка была успешна изменена!\n"
		                          "вернутьcя в меню - /doctor \nвыбрать новую роль - /start")
		await state.clear()

@doctor_r.callback_query(DoctorStates.change_appointment, DoctorBackCallback.filter(F.is_back == True))
async def backpacking(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text=msg.DOCTOR,
	                       reply_markup=kb.get_doctor_interface().as_markup())
	await state.set_state(DoctorStates.menu)

@doctor_r.callback_query(DoctorStates.change_appointment, DoctorBackCallback.filter(F.is_back == False))
async def end(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text='Отличная работа! \nвыбрать новую роль - /start')
	await state.clear()

#закрыть историю
@doctor_r.callback_query(DoctorStates.menu, DoctorInterfaceCallback.filter(F.is_close_history == True))
async def select_patient(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text="Выберите пациента:\n"
	                                                        "Список:\nФИО        Пол Возраст"
	                                                        + msg.get_names(db.get_patients()) +
	                                                        "\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
	await state.set_state(DoctorStates.patient_name_close)

@doctor_r.message(DoctorStates.patient_name_close)
async def patient_name_close(message: Message, state: FSMContext):
	patient_id = db.get_patient_id(message.text)
	if db.is_entrance_exist(patient_id):
		await message.answer(text="Пациент не оформлен!\n")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_doctor().as_markup())
		await state.set_state(DoctorStates.back)
	else:
		await state.update_data(patient_id=patient_id)
		entrance_id = db.get_entrance_id(patient_id)
		await state.update_data(entrance_id=entrance_id)
		await message.answer(text="Для дальнейшей работы введите своё ФИО:\n"
		                          "Список:" + msg.get_names(db.get_doctors()) +
		                          "\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
		await state.set_state(DoctorStates.select_diag_close)

@doctor_r.message(DoctorStates.select_diag_close)
async def select_diag_close(message: Message, state: FSMContext):
	doctor_id = db.get_doctor_id(message.text)
	await state.update_data(doctor_id=doctor_id)
	info = await state.get_data()
	await message.answer(text="Для прекращения лечения выберите один \nиз поставленных Вами диагнозов:\n"
	                          "Список:" +
	                          msg.get_names(db.get_diagnoses_from_history(info["doctor_id"], info["entrance_id"]))
	                          + "\nнет подходящего\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
	await state.set_state(DoctorStates.select_med_proc_close)

@doctor_r.message(DoctorStates.select_med_proc_close)
async def select_med_proc_close(message: Message, state: FSMContext):
	if message.text == "нет подходящего":
		await message.answer(text="Диагноз, лечние по которому Вы хотите прекратить, не был поставлен!\n")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_doctor().as_markup())
		await state.set_state(DoctorStates.back)
	else:
		diag_id = db.get_diagnos_id(message.text)
		await state.update_data(diag_id=diag_id)
		info = await state.get_data()
		history_id = db.get_history_id(info["doctor_id"], info["diag_id"], info["entrance_id"])
		await state.update_data(history_id=history_id)
		info = await state.get_data()
		if db.are_appointment_exist(info["entrance_id"]):#если есть назначения
			db.close_appointment_with_history(info["entrance_id"])
		await message.answer(text="По какой причине Вы прекращаете лечение?\n"
		                          "Здоров\nУмер"
		                          "\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
		await state.set_state(DoctorStates.close_history)

@doctor_r.message(DoctorStates.close_history)
async def select_condition(message: Message, state: FSMContext):
	await state.update_data(condition=message.text)
	info = await state.get_data()
	db.close_history(info["history_id"],info["condition"], info["entrance_id"])
	if message.text == "Умер":
		db.close_history_but_another(info["entrance_id"])
		db.update_doctor_active_if_died(info["doctor_id"], info["entrance_id"])
		db.close_entrance(info["condition"], info["entrance_id"])
		await message.answer(text="История закрыта!\n"
		                          "вернутьcя в меню - /doctor \nвыбрать новую роль - /start")
		await state.clear()
	if message.text == "Здоров":
		if db.is_uniq_doctor_for_create(info["doctor_id"], info["entrance_id"]):#все диагнозы у доктора вылечены
			db.update_doctor_active_if_cured(info["doctor_id"])
		if db.are_histories_exist(info["entrance_id"]):#пациент полностью здоров
			db.close_entrance(info["condition"], info["entrance_id"])
		await message.answer(text="История закрыта!\n"
		                          "вернутьcя в меню - /doctor \nвыбрать новую роль - /start")
		await state.clear()
	if (message.text != "Умер" and message.text != "Здоров"):
		await message.answer(text="Некорректная причина, закрытие истории отменено!\n")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_doctor().as_markup())
		await state.set_state(DoctorStates.back)

#уволиться
@doctor_r.callback_query(DoctorStates.menu, DoctorInterfaceCallback.filter(F.is_resign == True))
async def select_doctor(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text="Для дальнейшей работы введите своё ФИО:\n"
		                          "Список:" + msg.get_names(db.get_doctors()) +
		                          "\n<b>используйте CTRL+C и CTRL+V</b>", parse_mode='HTML')
	await state.set_state(DoctorStates.process_resign)

@doctor_r.message(DoctorStates.process_resign)
async def process_resign(message: Message, state: FSMContext):
	doctor_id = db.get_doctor_id(message.text)
	await state.update_data(doctor_id=doctor_id)
	db.flag_resign_doctor(message.text)
	active_patient = db.get_doctor_active_patient(message.text)
	if active_patient > 0:
		await message.answer(text="У Вас есть пациенты!\nПосле окончания их лечения мы сможем Вас уволить!")
		await message.answer(text="Хотите продолжить работу?", reply_markup=kb.get_back_doctor().as_markup())
		await state.set_state(DoctorStates.back)
	else:
		db.dismiss_doctor(message.text)
		await message.answer(text="Вы уволены!\n"
		                          "выбрать новую роль - /start")
		await state.clear()

@doctor_r.callback_query(DoctorStates.back, DoctorBackCallback.filter(F.is_back == True))
async def backpacking(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text=msg.DOCTOR,
	                       reply_markup=kb.get_doctor_interface().as_markup())
	await state.set_state(DoctorStates.menu)

@doctor_r.callback_query(DoctorStates.back, DoctorBackCallback.filter(F.is_back == False))
async def end(query: CallbackQuery, state: FSMContext, bot: Bot):
	await bot.send_message(chat_id=query.from_user.id, text='Отличная работа! \nвыбрать новую роль - /start')
	await state.clear()