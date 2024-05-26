from datetime import datetime, timedelta

from flask import g

from src.database.database import get_db


def get_greenhouse_measures(greenhouse_id, sensor_id, date_begin, date_end):
    cursor = g.db.cursor
    measures = []

    try:
        cursor.execute(
            "SELECT Measures.sensor_id, Measures.date, Measures.value, Sensors.type, Sensors.unit "
            "FROM Measures, Sensors "
            "WHERE Measures.sensor_id = Sensors.id  and Sensors.id = %s and Sensors.greenhouse_serial= %s and "
            "Measures.date BETWEEN %s and %s ",
            (sensor_id, greenhouse_id, date_begin, date_end))

        for sensor in cursor:
            measures.append(sensor)

    except Exception as e:
        print(f"Error when getting measures of greenhouse {greenhouse_id}: {e}")

    return measures


def get_greenhouse_actions(greenhouse_id, actuator_id, date_debut, date_fin):
    cursor = g.db.connect().cursor()

    try:
        cursor.execute(
            "SELECT Actions.actuator_id, Actions.date, Actions.value, Actuators.type "
            "FROM Actions, Actuators "
            "WHERE Actions.actuator_id = Actuators.id and Actuators.id= %s and Actuators.greenhouse_serial = %s and "
            "Actions.date BETWEEN %s and %s",
            (actuator_id, greenhouse_id, date_debut, date_fin))

        for (actuator_id, date, value, sensor_type) in cursor:
            print(f"Action in {greenhouse_id} the {date}, done by actuator {actuator_id}, {sensor_type} : {value}")

    except Exception as e:
        print(f"Error when getting actions of greenhouse : {greenhouse_id}: {e}")


def check_greenhouse_owner(user_name, greenhouse_serial):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT name "
            "FROM GreenHouses "
            "WHERE user_name= %s AND serial = %s",
            (user_name, greenhouse_serial)
        )
        name = cursor.fetchone()
        if name is None:
            return False
        return True

    except Exception as e:
        print(f"Error when checking greenhouse owner: {e}")
        return False


def get_greenhouses(user_name):
    db = get_db()
    cursor = db.cursor()
    greenhouses = {}

    try:
        cursor.execute(
            "SELECT serial, name "
            "FROM GreenHouses "
            "WHERE user_name = %s",
            (user_name,)
        )
        for (serial, greenhouse_name) in cursor:
            greenhouses[serial] = greenhouse_name

        return greenhouses

    except Exception as e:
        print(f"Error when getting greenhouses: {e}")


def get_sensors_greenhouse(greenhouse_serial):
    db = get_db()
    cursor = db.cursor()
    sensors = {}

    try:
        cursor.execute(
            "SELECT Sensors.id, Sensors.type "
            "FROM Sensors, GreenHouses "
            "WHERE greenhouse_serial = %s and GreenHouses.serial = Sensors.greenhouse_serial ",
            (greenhouse_serial,)
        )

        for (sensor_id, sensor_type) in cursor:
            sensors[sensor_id] = sensor_type

        return sensors

    except Exception as e:
        print(f"Error when getting sensors: {e}")


def get_actuators_greenhouse(greenhouse_serial):
    db = get_db()
    cursor = db.cursor()
    actuators = {}

    try:
        cursor.execute(
            "SELECT Actuators.id, Actuators.type "
            "FROM Actuators, GreenHouses "
            "WHERE greenhouse_serial = %s and GreenHouses.serial = Actuators.greenhouse_serial ",
            (greenhouse_serial,)
        )

        for (actuator_id, actuator_type) in cursor:
            actuators[actuator_id] = actuator_type

        return actuators

    except Exception as e:
        print(f"Error when getting actuators: {e}")


def get_data_sensors_since(serial_number, sensors_list, days):
    db = get_db()
    cursor = db.cursor()
    data = {}
    if not sensors_list:
        sensors_list = tuple(get_sensors_greenhouse(serial_number).keys())
    sensors_list_str = ', '.join(map(str, sensors_list))

    try:
        cursor.execute(
            "SELECT Sensors.id,  Measures.date, Measures.value "
            "FROM Sensors, GreenHouses, Measures "
            "WHERE greenhouse_serial = %s and GreenHouses.serial = Sensors.greenhouse_serial "
            "and Sensors.id = Measures.sensor_id and Sensors.id in (%s) and (Measures.date) > %s",
            (serial_number, sensors_list_str, datetime.now() - timedelta(days=days))
        )
        for (sensor_id, date, value) in cursor:
            if sensor_id not in data:
                data[sensor_id] = {}
            data[sensor_id][date] = value

        return data

    except Exception as e:
        print(f"Error when getting data: {e}")


def get_data_actuators_since(serial_number, actuators_list, days):
    db = get_db()
    cursor = db.cursor()
    data = {}
    if not actuators_list:
        actuators_list = tuple(get_actuators_greenhouse(serial_number).keys())
    actuators_list_str = ', '.join(map(str, actuators_list))

    try:
        cursor.execute(
            "SELECT Actuators.id,  Actions.date, Actions.value "
            "FROM Actuators, GreenHouses, Actions "
            "WHERE greenhouse_serial = %s and GreenHouses.serial = Actuators.greenhouse_serial "
            "and Actuators.id = Actions.actuator_id and Actuators.id in (%s) and (Actions.date) > %s",
            (serial_number, actuators_list_str, datetime.now() - timedelta(days=days))
        )
        for (actuator_id, date, value) in cursor:
            if actuator_id not in data:
                data[actuator_id] = {}
            data[actuator_id][date] = value

        return data

    except Exception as e:
        print(f"Error when getting data: {e}")


def get_sensor_type(sensor_id):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT type "
            "FROM Sensors "
            "WHERE id = %s",
            (sensor_id,)
        )
        sensor_type = cursor.fetchone()
        if sensor_type is None:
            return None
        return sensor_type[0]

    except Exception as e:
        print(f"Error when getting sensor type: {e}")
        return None


def get_actuator_type(actuator_id):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT type "
            "FROM Actuators "
            "WHERE id = %s",
            (actuator_id,)
        )
        actuator_type = cursor.fetchone()
        if actuator_type is None:
            return None
        return actuator_type[0]

    except Exception as e:
        print(f"Error when getting actuator type: {e}")
        return None


def get_greenhouse_name(serial_number):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT name "
            "FROM GreenHouses "
            "WHERE serial = %s",
            (serial_number,)
        )
        name = cursor.fetchone()
        if name is None:
            return None
        return name[0]

    except Exception as e:
        print(f"Error when getting greenhouse name: {e}")
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
