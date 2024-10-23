from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.db import create_db
from filters.callback_data import AdminInterfaceCallback, AdminBackCallback, DoctorInterfaceCallback, \
    DoctorBackCallback

db = create_db()

ADMIN = [('Список всех врачей', AdminInterfaceCallback(is_list_doctors=True)),
         ('Список всех отделений', AdminInterfaceCallback(is_list_departments=True)),
         ('Зарегистрировать пациента', AdminInterfaceCallback(is_add_patient=True)),
         ('Принять на работу врача', AdminInterfaceCallback(is_add_doctor=True)),
         ('Уволить врача', AdminInterfaceCallback(is_delete_doctor=True)),
         ('Создать отделение', AdminInterfaceCallback(is_create_department=True)),
         ('Добавить лекарство', AdminInterfaceCallback(is_add_medicine=True)),
         ('Добавить процедуру', AdminInterfaceCallback(is_add_procedure=True)),
         ('Добавить диагноз', AdminInterfaceCallback(is_add_diagnos=True)),
         ('Связать диагноз с лекарством или процедурой', AdminInterfaceCallback(is_connect_diagnos=True)),
         ('Отчёты', AdminInterfaceCallback(is_report=True))]

ADMIN_REPORT = [('Список врачей, чьи пациенты умирают', AdminInterfaceCallback(is_doctor_killed=True)),
                ('список лучших врачей по отделениям', AdminInterfaceCallback(is_great_doctor=True)),
                ('Частота болезней пациентов', AdminInterfaceCallback(is_frequency=True)),
                ('История болезни', AdminInterfaceCallback(is_all_history=True))]

ADMIN_BACK = [('Вернуться к меню', AdminBackCallback(is_back=True)),
              ('Закончить работу', AdminBackCallback(is_back=False))]



def get_admin_interface() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for title, callback_data in ADMIN:
        builder.button(text=title, callback_data=callback_data)
    builder.adjust(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    return builder

def get_admin_report() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for title, callback_data in ADMIN_REPORT:
        builder.button(text=title, callback_data=callback_data)
    builder.adjust(1, 1, 1, 1)
    return builder

def get_back_admin() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for (title, callback_data) in ADMIN_BACK:
        builder.button(text=title, callback_data=callback_data)
    builder.adjust(2)
    return builder

DOCTOR = [('Оформление пациента', DoctorInterfaceCallback(is_add_patient=True)),
            ('Поставить диагноз', DoctorInterfaceCallback(is_add_history=True)),
            ('Назначить лечение/изменить дозировку', DoctorInterfaceCallback(is_add_appointment=True)),
            ('Закрыть историю пациента', DoctorInterfaceCallback(is_close_history=True)),
            ('Хочу уволиться', DoctorInterfaceCallback(is_resign=True))]

DOCTOR_BACK = [('Вернуться к меню', DoctorBackCallback(is_back=True)),
               ('Закончить работу', DoctorBackCallback(is_back=False))]

DOCTOR_APPOINTMENT = [('Изменить дозировку', DoctorInterfaceCallback(is_change_dosage=True)),
                      ('Вернуться к меню', DoctorBackCallback(is_back=True)),
                      ('Закончить работу', DoctorBackCallback(is_back=False))]

def get_doctor_interface() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for title, callback_data in DOCTOR:
        builder.button(text=title, callback_data=callback_data)
    builder.adjust(1, 1, 1, 1, 1)
    return builder


def get_back_doctor() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for (title, callback_data) in DOCTOR_BACK:
        builder.button(text=title, callback_data=callback_data)
    builder.adjust(2)
    return builder

def get_doctor_appointment() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for (title, callback_data) in DOCTOR_APPOINTMENT:
        builder.button(text=title, callback_data=callback_data)
    builder.adjust(1, 1, 1)
    return builder