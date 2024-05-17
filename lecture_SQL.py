from connexion import SQL_connection

class SQL_lecture:

	def __init__(self):
		super().__init__()
		self.cursor = sql.cursor


	def afficher_mesures_serre(self, name_serre):
		"""Affiche les mesures de la serre name_serre"""

		try:
			self.cursor.execute("SELECT Measures.sensor_id, Measures.date, Measures.value, Sensors.type, Sensors.unit FROM Measures, Sensors WHERE Measures.sensor_id = Sensors.id and Sensors.greenhouse_name= %s", (name_serre,))
			for (sensor_id, date, value, type, unit) in self.cursor:
				print(f"Mesure dans {name_serre} le {date}, faite par le capteur {sensor_id}, {type} de {value} {unit}")

		except Exception as e:
			print(f"Erreur lors de l'affichage des mesures de la serre {name_serre}: {e}")


	def afficher_actions_serre(self, name_serre):
		"""Affiche les actions de la serre name_serre"""

		try:
			self.cursor.execute("SELECT Actions.actuator_id, Actions.date, Actions.value, Actuators.type FROM Actions, Actuators WHERE Actions.actuator_id = Actuators.id and Actuators.greenhouse_name= %s", (name_serre,))
			for (actuator_id, date, value, type) in self.cursor:
				print(f"Action dans {name_serre} le {date}, faite par l'actionneur {actuator_id}, {type} de {value}")

		except Exception as e:
			print(f"Erreur lors de l'affichage des actions de la serre {name_serre}: {e}")





if __name__ == '__main__':
	sql = SQL_connection()
	sql_lecture = SQL_lecture()
	sql_lecture.afficher_mesures_serre("serre1")
	print()
	sql_lecture.afficher_actions_serre("serre1")