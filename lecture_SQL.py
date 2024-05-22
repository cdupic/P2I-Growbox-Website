from connexion import SQL_connection
sql = SQL_connection()

class SQL_lecture:

	def __init__(self):
		super().__init__()
		self.cursor = sql.cursor


	def afficher_mesures_serre(self, greenhouse_id):
		"""Affiche les mesures de la serre name_serre"""
		liste_mesures = []
		dic_mesures ={"temperature": [], "soil_humidity": [], "light": [], "air_humidity": [], "O2": [], "water_level": []}
		try:
			self.cursor.execute("SELECT Measures.sensor_id, Measures.date, Measures.value, Sensors.type, Sensors.unit FROM Measures, Sensors WHERE Measures.sensor_id = Sensors.id and Sensors.serial_number= %s", (greenhouse_id,))
			for (sensor_id, date, value, type, unit) in self.cursor:
				print(f"Mesure dans {greenhouse_id} le {date}, faite par le capteur {sensor_id}, {type} de {value} {unit}")
				liste_mesures.append(f"Mesure dans {greenhouse_id} le {date}, faite par le capteur {sensor_id}, {type} de {value} {unit}")
				dic_mesures[type].append([value, date, unit])
			return (liste_mesures, dic_mesures)

		except Exception as e:
			print(f"Erreur lors de l'affichage des mesures de la serre {greenhouse_id}: {e}")



	def afficher_actions_serre(self, greenhouse_id):
		"""Affiche les actions de la serre name_serre"""

		try:
			self.cursor.execute("SELECT Actions.actuator_id, Actions.date, Actions.value, Actuators.type FROM Actions, Actuators WHERE Actions.actuator_id = Actuators.id and Actuators.serial_number= %s", (greenhouse_id,))
			for (actuator_id, date, value, type) in self.cursor:
				print(f"Action dans {greenhouse_id} le {date}, faite par l'actionneur {actuator_id}, {type} de {value}")

		except Exception as e:
			print(f"Erreur lors de l'affichage des actions de la serre {greenhouse_id}: {e}")






if __name__ == '__main__':
	sql_lecture = SQL_lecture()
	sql_lecture.afficher_mesures_serre("test_serial")
	print()
	sql_lecture.afficher_actions_serre("test_serial")