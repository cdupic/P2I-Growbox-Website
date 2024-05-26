from src.database.database import get_db


def get_history_greenhouse(greenhouse_serial):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    history = []

    try:
        cursor.execute(
            "SELECT Plants.name, GreenHousePlants.date_start, GreenHousePlants.date_end "
            "FROM Plants, GreenHousePlants "
            "WHERE GreenHousePlants.greenhouse_serial = %s and Plants.id = GreenHousePlants.plant_id "
            "and date_end is NOT NULL",
            (greenhouse_serial,)
        )

        for (dic) in cursor:
            history.append(dic)
        return history

    except Exception as e:
        print(f"Error when getting history: {e}")
        return None


def add_mix_plant(greenhouse_serial, list_plants):
    db = get_db()
    cursor = db.cursor()
    list_plants_id = list_plants[0]
    list_plants_units = list_plants[1]

    try:

        temperature_moy = soil_humidity_moy = air_humidity_moy = light_moy = O2_moy = 0
        nb_plants = sum(list_plants_units)
        serial_exist = False

        cursor.execute("SELECT serial FROM GreenHouses WHERE EXISTS (SELECT serial FROM GreenHouses WHERE serial = %s )"
                       , (greenhouse_serial,))
        for (serial,) in cursor:
            if serial:
                serial_exist = True

        # get the average of the plants' parameters
        for i in range(len(list_plants_id)):
            cursor.execute("SELECT temperature, soil_humidity, air_humidity, light, O2 FROM Plants WHERE id = %s",
                           (list_plants_id[i],))
            for (temperature, soil_humidity, air_humidity, light, O2,) in cursor:
                temperature_moy += temperature * list_plants_units[i]
                soil_humidity_moy += soil_humidity * list_plants_units[i]
                air_humidity_moy += air_humidity * list_plants_units[i]
                light_moy += light * list_plants_units[i]
                O2_moy += O2 * list_plants_units[i]

        # check if the greenhouse already exists, if it doesn't, should show an error on the website
        if serial_exist:
            cursor.execute("UPDATE GreenHouses "
                           "SET temperature = %s, soil_humidity = %s, air_humidity = %s, light = %s, O2 = %s, "
                           "plant_init_date = NOW() "
                           "WHERE serial = %s ",
                           (temperature_moy / nb_plants, soil_humidity_moy / nb_plants, air_humidity_moy / nb_plants,
                            light_moy / nb_plants, O2_moy / nb_plants, greenhouse_serial))
            db.commit()

        # add the relations in GreenHousePlants and update them if they already exist
        for plant_id in list_plants_id:

            plant_exist = False
            cursor.execute("SELECT plant_id, date_end "
                           "FROM GreenHousePlants WHERE EXISTS (SELECT plant_id FROM GreenHouses WHERE "
                           "plant_id = %s and greenhouse_serial = %s)"
                           , (plant_id, greenhouse_serial))
            for (id_plant, date_end) in cursor:
                if id_plant and date_end is None:
                    plant_exist = True

            if not plant_exist:
                cursor.execute("INSERT INTO GreenHousePlants (plant_id, greenhouse_serial) VALUES (%s , %s)",
                               (plant_id, greenhouse_serial))
                db.commit()

        # check if there are plants that are not in the list anymore :-> update the date_fin
        list_plant_id_to_end = []
        cursor.execute("SELECT plant_id "
                       "FROM GreenHousePlants WHERE greenhouse_serial = %s and date_end is NULL ",
                       (greenhouse_serial,))

        for (plant_id,) in cursor:
            list_plant_id_to_end.append(plant_id)

        for i in range(len(list_plants_id)):
            if list_plant_id_to_end[i] not in list_plants_id:
                cursor.execute("UPDATE GreenHousePlants SET date_end = NOW() "
                               "WHERE plant_id = %s and greenhouse_serial = %s and date_end is NULL",
                               (list_plant_id_to_end[i], greenhouse_serial))
                db.commit()

    except Exception as e:
        print(f"Error when adding plants: {e}")
        return False


def get_plants_greenhouse(greenhouse_serial):
    db = get_db()
    cursor = db.cursor()
    plants = {}

    try:
        cursor.execute(
            "SELECT Plants.name, GreenHousePlants.date_start "
            "FROM Plants, GreenHouses, GreenHousePlants "
            "WHERE GreenHouses.serial = GreenHousePlants.greenhouse_serial and Plants.id = GreenHousePlants.plant_id "
            "and greenhouse_serial = %s and date_end is NULL",
            (greenhouse_serial,)
        )

        for (plant_name, date_star) in cursor:
            plants[plant_name] = date_star
        return plants

    except Exception as e:
        print(f"Error when getting plants: {e}")
        return None


def get_data_plant():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    plants = {}

    try:
        cursor.execute(
            "SELECT DISTINCT(name), temperature, soil_humidity, air_humidity, light, O2 "
            "FROM Plants ")

        for (data) in cursor:
            plant_name = data['name']
            data.pop('name')
            dic_data = dict(data)
            plants[plant_name] = dic_data

        return plants

    except Exception as e:
        print(f"Error when getting plants: {e}")
        return None
