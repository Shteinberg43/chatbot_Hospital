from aiogram.filters.callback_data import CallbackData

# Админ
class AdminInterfaceCallback(CallbackData, prefix='admin-ui'):
    is_list_doctors: bool = False
    is_list_departments: bool = False
    is_add_patient: bool = False
    is_add_doctor: bool = False
    is_delete_doctor: bool = False
    is_create_department: bool = False
    is_add_medicine: bool = False
    is_add_procedure: bool = False
    is_add_diagnos: bool = False
    is_connect_diagnos: bool = False
    is_report: bool = False
    is_doctor_killed: bool = False
    is_great_doctor: bool = False
    is_frequency: bool = False
    is_all_history: bool = False


class AdminBackCallback(CallbackData, prefix='admin_back'):
    is_back: bool


# Врач

class DoctorInterfaceCallback(CallbackData, prefix='doctor-ui'):
    is_add_patient: bool = False
    is_add_history: bool = False
    is_add_appointment: bool = False
    is_change_dosage: bool = False
    is_close_history: bool = False
    is_resign: bool = False
class DoctorBackCallback(CallbackData, prefix='doctor_back'):
    is_back: bool
