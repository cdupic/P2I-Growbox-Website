from src.database.database import get_db

from datetime import timedelta


def get_plants_greenhouse(greenhouse_serial):
	db = get_db()
	cursor = db.cursor()
	plants = {}

	try:
		cursor.execute(
			"SELECT GreenHousePlants.id, Plants.id, GreenHousePlants.count, GreenHousePlants.date_start, Plants.date_bloom "
			"FROM Plants, GreenHousePlants "
			"WHERE Plants.id = GreenHousePlants.plant_id "
			"and GreenHousePlants.greenhouse_serial = %s and date_end is NULL",
			(greenhouse_serial,)
		)

		for (association_id, plant_id, count, date_start, date_bloom) in cursor:
			plants[association_id] = (plant_id, count, date_start.isoformat(), date_start + timedelta(days=date_bloom))
		return plants

	except Exception as e:
		print(f"Error when getting plants: {e}")
		return None


def get_history_greenhouse(greenhouse_serial):
	db = get_db()
	cursor = db.cursor()
	history = {}

	try:
		cursor.execute(
			"SELECT GreenHousePlants.id, Plants.id, Plants.name, GreenHousePlants.count, GreenHousePlants.date_start,"
			" GreenHousePlants.date_end "
			"FROM Plants, GreenHousePlants "
			"WHERE GreenHousePlants.greenhouse_serial = %s and Plants.id = GreenHousePlants.plant_id "
			"and date_end is NOT NULL",
			(greenhouse_serial,)
		)

		for (id_association, plant_id, plant_name, count, date_start, date_end) in cursor:
			history[id_association] = (plant_id, plant_name, count, date_start, date_end)
		return history

	except Exception as e:
		print(f"Error when getting history: {e}")
		return None


def get_data_plant():
	db = get_db()
	cursor = db.cursor()
	plants = {}

	try:
		cursor.execute(
			"SELECT id, name, temperature, soil_humidity, air_humidity, light "
			"FROM Plants ")

		for (id_plant, name, temperature, soil_humidity, air_humidity, light) in cursor:
			plants[id_plant] = (name, temperature/10, soil_humidity/10, air_humidity/10, light)

		return plants

	except Exception as e:
		print(f"Error when getting plants: {e}")
		return None


def add_association_plant(greenhouse_serial, list_plants, day_start=None):
	db = get_db()
	cursor = db.cursor()
	if list_plants[0] != '':
		list_plants_id = list_plants[0]
		list_plants_units = list_plants[1]

		try:
			if day_start is None:
				for i in range(len(list_plants_id)):
					cursor.execute(
						"INSERT INTO GreenHousePlants (plant_id, count, greenhouse_serial) VALUES (%s , %s, %s)",
						(int(list_plants_id[i]), int(list_plants_units[i]), greenhouse_serial))
					db.commit()
			else:
				for i in range(len(list_plants_id)):
					cursor.execute(
						"INSERT INTO GreenHousePlants (plant_id, count, greenhouse_serial, date_start) VALUES (%s , %s, %s, %s)",
						(int(list_plants_id[i]), int(list_plants_units[i]), greenhouse_serial, day_start))
					db.commit()

			return True
		except Exception as e:
			print(f"Error when adding plants: {e}")
			return False
	print('passé')


def terminate_association(list_association_id, list_new_count_association):
	db = get_db()
	cursor = db.cursor()
	if list_association_id != ['']:
		try:
			for i in range(len(list_association_id)):
				if int(list_new_count_association[i]) == 0:
					cursor.execute(
						"UPDATE GreenHousePlants SET date_end = CURRENT_TIMESTAMP() WHERE id = %s",
						(int(list_association_id[i]),))
					db.commit()
				else:
					cursor.execute(
						"UPDATE GreenHousePlants SET date_end = CURRENT_TIMESTAMP(), count = count - %s WHERE id = %s",
						(int(list_new_count_association[i]), int(list_association_id[i])))
					db.commit()

					cursor.execute(
						"SELECT plant_id, greenhouse_serial, date_start FROM GreenHousePlants WHERE id = %s",
						(int(list_association_id[i]),))

					plant_id, greenhouse_serial, date_start = cursor.fetchone()
					add_association_plant(greenhouse_serial, [[plant_id], [list_new_count_association[i]]], date_start)

			return True

		except Exception as e:
			print(f"Error when terminating association: {e}")
			return False


def actualiaze_greenhouse_targets(greenhouse_serial):
	db = get_db()
	cursor = db.cursor()
	dic_id_plants_count = {}
	for id_association, (id_plant, id_count, _, _) in get_plants_greenhouse(greenhouse_serial).items():
		dic_id_plants_count[id_association] = (id_plant, id_count)

	temperature_avg = 0
	soil_humidity_avg = 0
	air_humidity_avg = 0
	light_avg = 0
	sum_plants = 0
	for id_association, (id_plant, count) in dic_id_plants_count.items():
		sum_plants += count

	try:
		for id_association, (id_plant, count) in dic_id_plants_count.items():
			cursor.execute(
				"SELECT temperature, soil_humidity, air_humidity, light FROM Plants WHERE id = %s",
				(id_plant,))
			for temperature, soil_humidity, air_humidity, light in cursor:
				temperature_avg += temperature * count/sum_plants
				soil_humidity_avg += soil_humidity * count/sum_plants
				air_humidity_avg += air_humidity * count/sum_plants
				light_avg += light * count/sum_plants

		cursor.execute(
			"UPDATE GreenHouses SET temperature = %s, soil_humidity = %s, air_humidity = %s, light = %s,"
			"is_custom_config = 0, "
			"plant_init_date = UTC_TIMESTAMP() "
			" WHERE serial = %s",
			(temperature_avg, soil_humidity_avg, air_humidity_avg, light_avg, greenhouse_serial))
		db.commit()

	except Exception as e:
		print(f"Error when updating greenhouse: {e}")
		return False


def get_name_plant(plant_id):
	db = get_db()
	cursor = db.cursor()

	try:
		cursor.execute(
			"SELECT name FROM Plants WHERE id = %s",
			(plant_id,))
		name = cursor.fetchone()
		return name[0]

	except Exception as e:
		print(f"Error when getting name plant: {e}")
		return None
