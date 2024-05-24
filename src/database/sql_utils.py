# from flask import g
from src.database.test.sql_connexion_test import SQL_connection
from datetime import datetime


def get_greenhouse_measures(greenhouse_id, sensor_id, date_begin, date_end):
	# cursor = g.db.connect().cursor()
	# TODO : Modify to access database with g object
	sql_connection = SQL_connection()
	cursor = sql_connection.cursor

	measures = {"temperature": [], "soil_humidity": [], "light": [], "air_humidity": [], "O2": [], "water_level": []}
	try:

		cursor.execute(
			"SELECT Measures.sensor_id, Measures.date, Measures.value, Sensors.type, Sensors.unit "
			"FROM Measures, Sensors "
			"WHERE Measures.sensor_id = Sensors.id  and Sensors.id = %s and Sensors.serial_number= %s and "
			"Measures.date BETWEEN %s and %s ",
			(sensor_id, greenhouse_id, date_begin, date_end))

		for (sensor_id, date, value, sensor_type, unit) in cursor:
			print(f" Measure in {greenhouse_id} le {date}, done by sensor {sensor_id}, {sensor_type} : {value} {unit}")
			measures[sensor_type].append([value, date, unit])

		sql_connection.fermer_connexion_bd()

		return measures

	except Exception as e:
		print(f"Error when getting values of greenhouse : {greenhouse_id}: {e}")


def print_greenhouse_actions(greenhouse_id, actuator_id, date_debut, date_fin):
	# cursor = g.db.connect().cursor()
	# TODO : Modify to access database with g object
	sql_connection = SQL_connection()
	cursor = sql_connection.cursor

	try:
		cursor.execute(
			"SELECT Actions.actuator_id, Actions.date, Actions.value, Actuators.type "
			"FROM Actions, Actuators "
			"WHERE Actions.actuator_id = Actuators.id and Actuators.id= %s and Actuators.serial_number= %s and "
			"Actions.date BETWEEN %s and %s",
			(actuator_id, greenhouse_id, date_debut, date_fin))

		for (actuator_id, date, value, sensor_type) in cursor:
			print(f"Action in {greenhouse_id} the {date}, done by actuator {actuator_id}, {sensor_type} : {value}")

		sql_connection.fermer_connexion_bd()

	except Exception as e:
		print(f"Error when getting actions of greenhouse : {greenhouse_id}: {e}")


