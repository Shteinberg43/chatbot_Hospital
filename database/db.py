import sqlite3
from datetime import date, timedelta
from config import DATABASE_FILE
class DBquery:
	def __init__(self):
		self.db_file = DATABASE_FILE

	def _sql_query(self, query, *args):
		with sqlite3.connect(database=self.db_file) as connect:
			cursor = connect.cursor()
			cursor.execute(query, args)
			data = cursor.fetchall()
			connect.commit()
			return data
#departments
	def is_depart_exist(self, title: str) -> bool:
		query = f"""SELECT COUNT(title) FROM DEPARTMENT WHERE title = ? """
		return (False, True)[self._sql_query(query, title)[0][0] == 0]

	def create_department(self, title: str, beds: int) -> int:
		query = f"""INSERT INTO DEPARTMENT(title,numbers_of_bed) VALUES(?,?)"""
		self._sql_query(query, title, beds)
		query = f"""SELECT id FROM DEPARTMENT ORDER BY id DESC LIMIT 1;"""
		id_depart = self._sql_query(query)
		return id_depart[0][0]

	def get_departments(self):
		query = """SELECT title, numbers_of_bed FROM DEPARTMENT;"""
		data = self._sql_query(query)
		data = [(elem[0] + " " + str(elem[1])) for elem in data]
		return data

	def get_department_id(self, dep_title: str) -> int:
		query = f"""SELECT id FROM DEPARTMENT WHERE title = ?"""
		department_id = self._sql_query(query, dep_title)
		return department_id[0][0]

	def get_department_bed(self, id_dep: int) -> int:
		query = f"""SELECT numbers_of_bed FROM DEPARTMENT WHERE id = ?"""
		department_bed = self._sql_query(query, id_dep)
		return department_bed[0][0]

	def update_department_bed(self, id_dep: int, a: int):
		query = f"""SELECT numbers_of_bed FROM DEPARTMENT WHERE id = ?"""
		department_bed = self._sql_query(query, id_dep)
		num_bed = department_bed[0][0] + a
		query = f"""UPDATE DEPARTMENT SET numbers_of_bed = ? WHERE id = ?"""
		self._sql_query(query, num_bed, id_dep)


#diagnoses
	def is_diag_exist(self, title: str) -> bool:
		query = f"""SELECT COUNT(title) FROM DIAGNOSIS WHERE title = ? """
		return (False, True)[self._sql_query(query, title)[0][0] == 0]

	def create_diagnos(self, id_dep: int, title: str) -> int:
		query = f"""INSERT INTO DIAGNOSIS(id_department,title) VALUES(?,?)"""
		self._sql_query(query, id_dep, title)
		query = f"""SELECT id FROM DIAGNOSIS ORDER BY id DESC LIMIT 1;"""
		id_diag = self._sql_query(query)
		return id_diag[0][0]

	def get_diagnos(self):
		query = """SELECT title FROM DIAGNOSIS;"""
		data = self._sql_query(query)
		data = [elem[0] for elem in data]
		return data

	def get_diagnos_id(self, dep_title: str) -> int:
		query = f"""SELECT id FROM DIAGNOSIS WHERE title = ?"""
		diag_id = self._sql_query(query, dep_title)
		return diag_id[0][0]
#medicines and procedure
	def is_medic_exist(self, title: str) -> bool:
		query = f"""SELECT COUNT(title) FROM PROC_MEDICAT WHERE title = ? """
		return (False, True)[self._sql_query(query, title)[0][0] == 0]

	def is_med_proc_exist(self,diag_id: int, med_id: int) -> bool:
		query = f"""SELECT COUNT(id_diag) FROM DIAG_PROC_OR_MEDICAT WHERE (id_diag = ? AND id_medic = ?) """
		return (False, True)[self._sql_query(query, diag_id, med_id)[0][0] == 0]

	def create_connect_diag_med(self,diag_id: int, med_id: int):
		query = f"""INSERT INTO DIAG_PROC_OR_MEDICAT(id_diag,id_medic) VALUES(?,?)"""
		self._sql_query(query, diag_id, med_id)

	def get_specific_med(self, diag_id:  int):
		query = f"""SELECT title FROM PROC_MEDICAT WHERE (
		id IN (SELECT id_medic FROM DIAG_PROC_OR_MEDICAT WHERE id_diag = ?) AND is_medications = 1);"""
		data = self._sql_query(query, diag_id)
		data = [elem[0] for elem in data]
		return data

	def get_specific_proc(self, diag_id:  int):
		query = f"""SELECT title FROM PROC_MEDICAT WHERE (
		id IN (SELECT id_medic FROM DIAG_PROC_OR_MEDICAT WHERE id_diag = ?) AND is_medications = 0);"""
		data = self._sql_query(query, diag_id)
		data = [elem[0] for elem in data]
		return data

	def create_medicine(self, max_dos: int, title: str) -> int:
		query = f"""INSERT INTO PROC_MEDICAT(title,max_daily_dosage,is_medications) VALUES(?,?,?)"""
		is_med = 1
		self._sql_query(query, title, max_dos, is_med)
		query = f"""SELECT id FROM PROC_MEDICAT ORDER BY id DESC LIMIT 1;"""
		id_medic = self._sql_query(query)
		return id_medic[0][0]

	def create_procedure(self, max_dos: int, title: str) -> int:
		query = f"""INSERT INTO PROC_MEDICAT(title,max_daily_dosage,is_medications) VALUES(?,?,?)"""
		is_proc = 0
		self._sql_query(query, title, max_dos, is_proc)
		query = f"""SELECT id FROM PROC_MEDICAT ORDER BY id DESC LIMIT 1;"""
		id_proc = self._sql_query(query)
		return id_proc[0][0]

	def get_med_proc(self):
		query = """SELECT title FROM PROC_MEDICAT;"""
		data = self._sql_query(query)
		data = [elem[0] for elem in data]
		return data

	def get_med(self):
		query = """SELECT title FROM PROC_MEDICAT WHERE is_medications = 1;"""
		data = self._sql_query(query)
		data = [elem[0] for elem in data]
		return data

	def get_proc(self):
		query = """SELECT title FROM PROC_MEDICAT WHERE is_medications = 0;"""
		data = self._sql_query(query)
		data = [elem[0] for elem in data]
		return data

	def get_med_proc_id(self, dep_title: str) -> int:
		query = f"""SELECT id FROM PROC_MEDICAT WHERE title = ?"""
		medic_id = self._sql_query(query, dep_title)
		return medic_id[0][0]

#doctors
	def is_doctor_exist(self, name: str) -> bool:
		query = f"""SELECT COUNT(name) FROM DOCTORS WHERE name = ? """
		return (False, True)[self._sql_query(query, name)[0][0] == 0]

	def get_doctor_id(self, name: str) -> int:
		query = f"""SELECT id FROM DOCTORS WHERE name = ?"""
		doctor_id = self._sql_query(query, name)
		return doctor_id[0][0]
	def is_doctor_have_patient(self, title: str) -> bool:
		query = f"""SELECT COUNT(name) FROM DOCTORS WHERE (name = ? AND num_of_active = ?) """
		return (False, True)[self._sql_query(query, title, 0)[0][0] == 0]

	def get_doctor_active_patient(self, name: str) -> int:
		query = f"""SELECT num_of_active FROM DOCTORS WHERE name = ?"""
		doctor_id = self._sql_query(query, name)
		return doctor_id[0][0]

	def get_doctors_department_id(self, id_doc: int) -> int:
		query = f"""SELECT id_department FROM DOCTORS WHERE id = ?"""
		dep_id = self._sql_query(query, id_doc)
		return dep_id[0][0]

	def get_doctors_diagnose(self, id_doc: int):
		dep_id = self.get_doctors_department_id(id_doc)
		query = f"""SELECT title FROM DIAGNOSIS WHERE id_department = ?"""
		data = self._sql_query(query, dep_id)
		data = [elem[0] for elem in data]
		return data

	def update_doctor_active_patient(self, id_doc: int):
		query = f"""UPDATE DOCTORS SET num_of_active = num_of_active + 1 WHERE id = ?"""
		self._sql_query(query, id_doc)

	def get_doctors(self):
		query = """SELECT name, profession FROM Doctors WHERE date_of_resign is NULL;"""
		data = self._sql_query(query)
		data = [(elem[0] + " " + elem[1]) for elem in data]
		return data

	def get_doctors_killed(self):
		query = """SELECT name, profession, num_of_killed FROM Doctors WHERE (NOT num_of_killed = 0 AND date_of_resign is NULL);"""
		data = self._sql_query(query)
		data = [(elem[0] + " " + elem[1] + "  " + str(elem[2])) for elem in data]
		return data


	def get_doctors_great_in_depart(self):
		query = """SELECT d.id, d.id_department, d.name, d.profession, (d.num_of_cured - d.num_of_killed) AS difference 
		FROM DOCTORS d JOIN (SELECT id_department, MAX(num_of_cured - num_of_killed) AS max_difference 
		FROM DOCTORS GROUP BY id_department) AS dept_best ON d.id_department = dept_best.id_department 
		AND (d.num_of_cured - d.num_of_killed) = dept_best.max_difference WHERE date_of_resign is NULL
		ORDER BY d.id_department, difference DESC"""
		data = self._sql_query(query)
		data = [(elem[2] + " " + elem[3] + "  " + str(elem[4])) for elem in data]
		return data

	def get_frequency_diag(self, begin_date: str, end_date: str):
		query = """SELECT D.title, COUNT(MH.id_diag) AS frequency 
		FROM MEDICAL_HISTORY MH JOIN DIAGNOSIS D ON MH.id_diag = D.id
		WHERE MH.begin_date >= ? AND MH.end_date <= ? GROUP BY D.title
		ORDER BY frequency DESC"""
		data = self._sql_query(query, begin_date, end_date)
		data = [(elem[0] + "  " + str(elem[1])) for elem in data]
		return data

	def get_history_year(self, year: str):
		begin_date = year + "-01-01"
		end_date = year + "-12-31"
		query = f"""SELECT DP.title, COUNT(CASE WHEN (MH.begin_date >= ? AND MH.end_date <= ?) THEN 1 END) AS total_entrances,
		COUNT(CASE WHEN (MH.condition = "Здоров" AND MH.begin_date >= ? AND MH.end_date <= ?) 
		THEN 1 END) AS count_healthy,
        COUNT(CASE WHEN (MH.condition = "Умер" AND MH.begin_date >= ? AND MH.end_date <= ?) 
        THEN 1 END) AS count_deceased,
        COUNT(CASE WHEN (MH.condition = "Умер по другой причине" AND MH.begin_date >= ? AND MH.end_date <= ?) 
        THEN 1 END) AS count_deceased_other
        FROM MEDICAL_HISTORY MH JOIN DIAGNOSIS DI ON MH.id_diag = DI.id
        JOIN DEPARTMENT DP ON DI.id_department = DP.id
        GROUP BY MH.id_diag, DI.id_department"""
		data = self._sql_query(query, begin_date, end_date, begin_date, end_date, begin_date, end_date, begin_date, end_date)
		data = [(elem[0] + "\n        " + str(elem[1]) + "        " + str(elem[2]) + "        " + str(elem[3]) + "        " + str(elem[4])) for elem in data]
		return data

	def get_history(self):
		query = f"""SELECT DP.title, COUNT(*) AS total_entrances,
		COUNT(CASE WHEN MH.condition = "Здоров" THEN 1 END) AS count_healthy,
        COUNT(CASE WHEN MH.condition = "Умер" THEN 1 END) AS count_deceased,
        COUNT(CASE WHEN MH.condition = "Умер по другой причине" THEN 1 END) AS count_deceased_other
        FROM MEDICAL_HISTORY MH JOIN DIAGNOSIS DI ON MH.id_diag = DI.id
        JOIN DEPARTMENT DP ON DI.id_department = DP.id
        GROUP BY MH.id_diag, DI.id_department"""
		data = self._sql_query(query)
		data = [(elem[0] + "\n        " + str(elem[1]) + "        " + str(elem[2]) + "        " + str(elem[3]) + "        " + str(elem[4])) for elem in data]
		return data

	def create_doctor(self, id_dep: int, name: str, prof: str) -> int:
		resign = 0
		date_employ =date.today().strftime('%Y-%m-%d')
		num_cur = 0
		num_kil = 0
		num_act = 0
		query = f"""INSERT INTO DOCTORS(id_department,name,profession,resign,
		date_of_employment,num_of_cured,num_of_killed,num_of_active) VALUES(?,?,?,?,?,?,?,?)"""
		self._sql_query(query, id_dep, name, prof, resign, date_employ, num_cur, num_kil, num_act)
		query = f"""SELECT id FROM DOCTORS ORDER BY id DESC LIMIT 1;"""
		id_doctor = self._sql_query(query)
		return id_doctor[0][0]

	def flag_resign_doctor(self, name: str):
		query = f"""UPDATE DOCTORS SET resign = 1 WHERE name = ?"""
		self._sql_query(query, name)

	def dismiss_doctor(self, name: str):
		date_resign = date.today().strftime('%Y-%m-%d')
		query = f"""UPDATE DOCTORS SET date_of_resign = ? WHERE name = ?"""
		self._sql_query(query, date_resign, name)



#patients
	def is_patient_exist(self, title: str) -> bool:
		query = f"""SELECT COUNT(name) FROM PATIENT WHERE name = ? """
		return (False, True)[self._sql_query(query, title)[0][0] == 0]

	def get_patient_id(self, name: str) -> int:
		query = f"""SELECT id FROM PATIENT WHERE name = ?"""
		patient_id = self._sql_query(query, name)
		return patient_id[0][0]

	def get_patients(self):
		query = """SELECT name, gender, age FROM PATIENT;"""
		data = self._sql_query(query)
		data = [(elem[0] + " " + elem[1] + " " + str(elem[2])) for elem in data]
		return data
	def create_patient(self, name: str, gender: str, age: int) -> int:
		query = f"""INSERT INTO PATIENT(name,gender,age) VALUES(?,?,?)"""
		self._sql_query(query, name, gender, age)
		query = f"""SELECT id FROM PATIENT ORDER BY id DESC LIMIT 1;"""
		id_patient = self._sql_query(query)
		return id_patient[0][0]

#entrance
	def is_entrance_exist(self, id_patient: int) -> bool:
		query = f"""SELECT COUNT(id) FROM ENTRANCE WHERE (id_patient = ? AND end_date is NULL)"""
		return (False, True)[self._sql_query(query, id_patient)[0][0] == 0]

	def create_entrance(self, id_dep: int, id_patient: int, problems: str) -> int:
		begin_date =date.today().strftime('%Y-%m-%d')
		condition = "Лечение"
		query = f"""INSERT INTO ENTRANCE(id_first_department, id_patient, begin_date, condition, first_complaint) VALUES(?,?,?,?,?)"""
		self._sql_query(query, id_dep, id_patient, begin_date, condition, problems)
		query = f"""SELECT id FROM ENTRANCE ORDER BY id DESC LIMIT 1;"""
		id_entrance = self._sql_query(query)
		return id_entrance[0][0]

	def get_entrance_id(self, name: int) -> int:
		query = f"""SELECT id FROM ENTRANCE WHERE (id_patient = ? AND end_date is NULL)"""
		entrance_id = self._sql_query(query, name)
		return entrance_id[0][0]

	def close_entrance(self, condition: str, id_entrance: int):
		end_date = date.today().strftime('%Y-%m-%d')
		query = f"""UPDATE ENTRANCE SET end_date = ?, condition = ? WHERE id = ?"""
		self._sql_query(query,  end_date, condition, id_entrance)
		query = f"""UPDATE DEPARTMENT SET numbers_of_bed = numbers_of_bed + 1
				WHERE id IN (SELECT id_first_department FROM ENTRANCE WHERE id = ? ) """
		self._sql_query(query, id_entrance)

#medical history
	def is_history_exist(self, id_doc: int, id_diag: int, id_entrance: int) -> bool:
		query = f"""SELECT COUNT(id) FROM MEDICAL_HISTORY 
		WHERE (id_doctor = ? AND id_diag = ? AND id_entrance = ? AND end_date is NULL)"""
		return (False, True)[self._sql_query(query, id_doc, id_diag, id_entrance)[0][0] == 0]

	def are_histories_exist(self, id_entrance: int) -> bool:
		query = f"""SELECT COUNT(id) FROM MEDICAL_HISTORY 
		WHERE (id_entrance = ? AND end_date is NULL)"""
		return (False, True)[self._sql_query(query, id_entrance)[0][0] == 0]

	def get_history_id(self, id_doc: int, id_diag: int, id_entrance: int) -> int:
		query = f"""SELECT id FROM MEDICAL_HISTORY 
		WHERE (id_doctor = ? AND id_diag = ? AND id_entrance = ? AND end_date is NULL)"""
		entrance_id = self._sql_query(query, id_doc, id_diag, id_entrance)
		return entrance_id[0][0]
	def create_history(self, id_doc: int, id_diag: int, id_entrance: int) -> int:
		begin_date =date.today().strftime('%Y-%m-%d')
		condition = "Лечение"
		query = f"""INSERT INTO MEDICAL_HISTORY(id_doctor, id_diag, id_entrance, begin_date, condition) VALUES(?,?,?,?,?)"""
		self._sql_query(query, id_doc, id_diag, id_entrance, begin_date, condition)
		query = f"""SELECT id FROM MEDICAL_HISTORY ORDER BY id DESC LIMIT 1;"""
		id_history = self._sql_query(query)
		return id_history[0][0]

	def get_diagnoses_from_history(self, id_doc: int, id_entrance: int):
		query = f"""SELECT title FROM DIAGNOSIS WHERE id IN (SELECT id_diag FROM MEDICAL_HISTORY 
		WHERE (id_doctor = ? AND id_entrance = ? AND end_date is NULL))"""
		diag = self._sql_query(query, id_doc, id_entrance)
		diag = [elem[0] for elem in diag]
		return diag

	def close_history(self, id_history: int, condition: str, id_entrance: int):
		end_date =date.today().strftime('%Y-%m-%d')
		query = f"""UPDATE MEDICAL_HISTORY SET end_date = ?, condition = ? WHERE id = ?"""
		self._sql_query(query,  end_date, condition, id_history)

	def close_history_but_another(self,  id_entrance: int):
		end_date =date.today().strftime('%Y-%m-%d')
		condition = "Умер по другой причине"
		query = f"""UPDATE MEDICAL_HISTORY SET end_date = ?, condition = ? 
		WHERE (id_entrance = ? AND end_date is NULL)"""
		self._sql_query(query,  end_date, condition, id_entrance)

	def is_uniq_doctor_for_create(self, id_doc: int, id_entrance: int) -> bool:
		query = f"""SELECT COUNT(id) FROM MEDICAL_HISTORY 
		WHERE (id_doctor = ? AND id_entrance = ? AND end_date is NULL)"""
		return (False, True)[self._sql_query(query, id_doc, id_entrance)[0][0] == 0]
	def get_uniq_doctor(self, id_entrance: int):
		condition = "Здоров"
		query = f"""SELECT DISTINCT id_doctor FROM MEDICAL_HISTORY 
		WHERE ( id_entrance = ? AND NOT condition = ?)"""
		doctor_id = self._sql_query(query,  id_entrance, condition)
		doctor_id = [str(elem[0]) for elem in doctor_id]
		return doctor_id

	def update_doctor_active_if_died(self, id_doc: int, id_entrance: int):
		doctor_id = self.get_uniq_doctor(id_entrance)
		query = f"""UPDATE DOCTORS SET num_of_active = num_of_active - 1 WHERE id IN ({','.join(doctor_id)})"""
		self._sql_query(query)
		query = f"""UPDATE DOCTORS SET num_of_killed = num_of_killed + 1 WHERE id = ? """
		self._sql_query(query, id_doc)

	def update_doctor_active_if_cured(self, id_doc: int):
		query = f"""UPDATE DOCTORS SET num_of_active = num_of_active - 1 WHERE id = ?"""
		self._sql_query(query, id_doc)
		query = f"""UPDATE DOCTORS SET num_of_cured = num_of_cured + 1 WHERE id = ?"""
		self._sql_query(query, id_doc)

#appointment
	def is_appointment_exist(self, id_hist: int, id_medic: int) -> bool:
		query = f"""SELECT COUNT(id) FROM APPOINTMENT
		WHERE (id_history = ? AND id_medic = ? AND end_date is NULL)"""
		return (False, True)[self._sql_query(query, id_hist, id_medic)[0][0] == 0]
	def are_appointment_exist(self, id_entrance: int) -> bool:
		#query = f"""SELECT COUNT(id) FROM APPOINTMENT
		#WHERE (id_history = ? AND end_date is NULL)"""
		query = f"""SELECT COUNT(id) FROM APPOINTMENT WHERE 
				(id_history IN (SELECT id FROM MEDICAL_HISTORY
				WHERE (id_entrance = ? AND end_date is NULL)) AND end_date is NULL)"""
		return (False, True)[self._sql_query(query, id_entrance)[0][0] > 0]
	def get_appointment_id(self, id_hist: int, id_medic: int) -> int:
		query = f"""SELECT id FROM APPOINTMENT 
		WHERE (id_history = ? AND id_medic = ? AND end_date is NULL)"""
		appointment_id = self._sql_query(query, id_hist, id_medic)
		return appointment_id[0][0]
	def create_appointment(self, id_hist: int, id_medic: int, dosage: int) -> int:
		begin_date =date.today().strftime('%Y-%m-%d')
		query = f"""INSERT INTO APPOINTMENT(id_history, id_medic, daily_dosage, begin_date) VALUES(?,?,?,?)"""
		self._sql_query(query, id_hist, id_medic, dosage, begin_date)
		query = f"""SELECT id FROM APPOINTMENT ORDER BY id DESC LIMIT 1;"""
		id_history = self._sql_query(query)
		return id_history[0][0]
	def close_appointment(self, id_appointment: int):
		now = date.today()
		one_day = timedelta(1)
		end_date = (now - one_day).strftime('%Y-%m-%d')
		query = f"""UPDATE APPOINTMENT SET end_date = ? WHERE id = ?"""
		self._sql_query(query, end_date, id_appointment)
	def close_appointment_with_history(self, id_entrance: int):
		end_date = date.today().strftime('%Y-%m-%d')
		#query = f"""UPDATE APPOINTMENT SET end_date = ? WHERE id_history = ?"""
		query = f"""UPDATE APPOINTMENT SET end_date = ? WHERE
		        (id_history IN (SELECT id FROM MEDICAL_HISTORY 
		        WHERE (id_entrance = ? AND end_date is NULL)) AND end_date is NULL)"""
		self._sql_query(query, end_date, id_entrance)
	def get_appointment_dosage(self, id: int) -> int:
		query = f"""SELECT daily_dosage FROM APPOINTMENT WHERE id = ?"""
		dosage = self._sql_query(query, id)
		return dosage[0][0]
	def get_max_possible_dosage(self, id_entrance: int, id_medic: int) -> int:
		query = f"""SELECT id FROM APPOINTMENT WHERE (id_history IN (SELECT id FROM MEDICAL_HISTORY
		 WHERE (id_entrance = ? AND end_date is NULL)) AND id_medic = ? AND end_date is NULL)"""
		id_appointments = self._sql_query(query, id_entrance, id_medic)
		id_appointments = [str(elem[0]) for elem in id_appointments]
		if len(id_appointments) == 0:
			sum_dosage = 0
		else:
			query = f"""SELECT SUM(daily_dosage) FROM APPOINTMENT WHERE id IN ({','.join(id_appointments)})"""
			sum_dosage = self._sql_query(query)
			sum_dosage = sum_dosage[0][0]
		query = f"""SELECT max_daily_dosage FROM PROC_MEDICAT WHERE id = ?;"""
		max_dosage = self._sql_query(query, id_medic)
		max_dosage = max_dosage[0][0]
		possible_dosage = max_dosage - sum_dosage
		return possible_dosage
def create_db() -> DBquery:
	if not hasattr(create_db, 'db'):
		setattr(create_db, 'db', DBquery())
	return create_db.db
def sql_make_tables():
	with sqlite3.connect(DATABASE_FILE) as db:
		cursor = db.cursor()
		query1 = """CREATE TABLE  IF NOT EXISTS DEPARTMENT(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT,
		numbers_of_bed INTEGER);"""
		query2 = """CREATE TABLE  IF NOT EXISTS DIAGNOSIS(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				id_department INTEGER,
				title TEXT,
				FOREIGN KEY(id_department) REFERENCES DEPARTMENT(id));"""
		query3 = """CREATE TABLE  IF NOT EXISTS PROC_MEDICAT(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				title TEXT,
				max_daily_dosage INTEGER,
				is_medications INTEGER);"""
		query4 = """CREATE TABLE  IF NOT EXISTS DIAG_PROC_OR_MEDICAT(
				id_diag INTEGER,
				id_medic INTEGER,
				FOREIGN KEY(id_diag) REFERENCES DIAGNOSIS(id),
				FOREIGN KEY(id_medic) REFERENCES PROC_MEDICAT(id));"""
		query5 = """CREATE TABLE  IF NOT EXISTS PATIENT(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT,
				gender TEXT,
				age INTEGER);"""
		query6 = """CREATE TABLE  IF NOT EXISTS ENTRANCE(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				id_first_department INTEGER,
				id_patient INTEGER,
				begin_date INTEGER,
				end_date INTEGER,
				FOREIGN KEY(id_first_department) REFERENCES DEPARTMENT(id),
				FOREIGN KEY(id_patient) REFERENCES PATIENT(id));"""
		query7 = """CREATE TABLE  IF NOT EXISTS DOCTRORS(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				id_department INTEGER,
				name TEXT,
				profession TEXT,
				resign INTEGER,
				date_of_employment INTEGER,
				date_of_resign INTEGER,
				num_of_cured INTEGER,
				num_of_killed INTEGER,
				num_of_active INTEGER,
				FOREIGN KEY(id_department) REFERENCES DEPARTMENT(id));"""
		query8 = """CREATE TABLE  IF NOT EXISTS MEDICAL_HISTORY(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				id_doctor INTEGER,
				id_diag INTEGER,
				id_entrance INTEGER,
				begin_date INTEGER,
				end_date INTEGER,
				condition TEXT,
				FOREIGN KEY(id_doctor) REFERENCES DOCTORS(id),
				FOREIGN KEY(id_diag) REFERENCES DIAGNOSIS(id),
				FOREIGN KEY(id_entrance) REFERENCES ENTRANCE(id));"""
		query9 = """CREATE TABLE  IF NOT EXISTS APPOINTMENT(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				id_history INTEGER,
				id_medic INTEGER,
				daily_dosage INTEGER,
				begin_date INTEGER,
				end_date INTEGER,
				FOREIGN KEY(id_history) REFERENCES MEDICAL_HISTORY(id),
				FOREIGN KEY(id_medic) REFERENCES PROC_MEDICAT(id));"""
		cursor.execute(query1)
		cursor.execute(query2)
		cursor.execute(query3)
		cursor.execute(query4)
		cursor.execute(query5)
		cursor.execute(query6)
		cursor.execute(query7)
		cursor.execute(query8)
		cursor.execute(query9)
		db.commit()

