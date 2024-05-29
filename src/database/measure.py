from datetime import datetime, timedelta

from flask import g

from src.database.database import get_db
from src.utils.measure import convert_actuator_type_to_french
from src.utils.measure import convert_sensor_type_to_french


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
            sensors[sensor_id] = convert_sensor_type_to_french(sensor_type)

    except Exception as e:
        print(f"Error when getting sensors: {e}")

    return sensors


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
            actuators[actuator_id] = convert_actuator_type_to_french(actuator_type)

    except Exception as e:
        print(f"Error when getting actuators: {e}")

    return actuators


def get_data_sensors_since(serial_number, sensors_list, days, day_start=None, day_end=None):
    db = get_db()
    cursor = db.cursor()
    data = {}
    if not sensors_list:
        sensors_list = tuple(get_sensors_greenhouse(serial_number).keys())
    sensors_list_str = ', '.join(map(str, sensors_list))

    try:
        if not day_start and not day_end:
            cursor.execute(
                "SELECT Sensors.id,  Measures.date, Measures.value "
                "FROM Sensors, GreenHouses, Measures "
                "WHERE greenhouse_serial = %s "
                "  AND GreenHouses.serial = Sensors.greenhouse_serial "
                "  AND Sensors.id = Measures.sensor_id "
                "  AND Sensors.id in (%s) "
                "  AND Measures.date >= %s",
                (serial_number, sensors_list_str, datetime.utcnow() - timedelta(days=days))
            )
            for (sensor_id, date, value) in cursor:
                if sensor_id not in data:
                    data[sensor_id] = {}
                data[sensor_id][date] = value
        else:
            cursor.execute(
                "SELECT Sensors.id,  Measures.date, Measures.value "
                "FROM Sensors, GreenHouses, Measures "
                "WHERE greenhouse_serial = %s and GreenHouses.serial = Sensors.greenhouse_serial "
                "and Sensors.id = Measures.sensor_id and Sensors.id in (%s) and (Measures.date) BETWEEN %s and %s",
                (serial_number, sensors_list_str, day_start, day_end)
            )
            for (sensor_id, date, value) in cursor:
                if sensor_id not in data:
                    data[sensor_id] = {}
                data[sensor_id][date] = value

        return data

    except Exception as e:
        print(f"Error when getting data: {e}")


def get_data_actuators_since(greenhouse_serial, actuators_list, days, day_start=None, day_end=None):
    db = get_db()
    cursor = db.cursor()
    data = {}
    if not actuators_list:
        actuators_list = tuple(get_actuators_greenhouse(greenhouse_serial).keys())
    actuators_list_str = ', '.join(map(str, actuators_list))

    try:
        if not day_start and not day_end:
            cursor.execute(
                "SELECT Actuators.id,  Actions.date, Actions.value "
                "FROM Actuators, GreenHouses, Actions "
                "WHERE greenhouse_serial = %s and GreenHouses.serial = Actuators.greenhouse_serial "
                "and Actuators.id = Actions.actuator_id and Actuators.id in (%s) and (Actions.date) > %s",
                (greenhouse_serial, actuators_list_str, datetime.now() - timedelta(days=days))
            )
            for (actuator_id, date, value) in cursor:
                if actuator_id not in data:
                    data[actuator_id] = {}
                data[actuator_id][date] = value

        else:
            cursor.execute(
                "SELECT Actuators.id,  Actions.date, Actions.value "
                "FROM Actuators, GreenHouses, Actions "
                "WHERE greenhouse_serial = %s and GreenHouses.serial = Actuators.greenhouse_serial "
                "and Actuators.id = Actions.actuator_id and Actuators.id in (%s) and (Actions.date) BETWEEN %s and %s",
                (greenhouse_serial, actuators_list_str, day_start, day_end)
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


# ARE THEY STILL USEFUL ??


def get_greenhouse_actions(greenhouse_serial, actuator_id, date_debut, date_fin):
    cursor = g.db.connect().cursor()

    try:
        cursor.execute(
            "SELECT Actions.actuator_id, Actions.date, Actions.value, Actuators.type "
            "FROM Actions, Actuators "
            "WHERE Actions.actuator_id = Actuators.id and Actuators.id= %s and Actuators.greenhouse_serial = %s and "
            "Actions.date BETWEEN %s and %s",
            (actuator_id, greenhouse_serial, date_debut, date_fin))

        for (actuator_id, date, value, sensor_type) in cursor:
            print(f"Action in {greenhouse_serial} the {date}, done by actuator {actuator_id}, {sensor_type} : {value}")

    except Exception as e:
        print(f"Error when getting actions of greenhouse : {greenhouse_serial}: {e}")


def get_greenhouse_measures(greenhouse_serial, sensor_id, date_begin, date_end):
    cursor = g.db.cursor
    measures = []

    try:
        cursor.execute(
            "SELECT Measures.sensor_id, Measures.date, Measures.value, Sensors.type "
            "FROM Measures, Sensors "
            "WHERE Measures.sensor_id = Sensors.id  and Sensors.id = %s and Sensors.greenhouse_serial= %s and "
            "Measures.date BETWEEN %s and %s ",
            (sensor_id, greenhouse_serial, date_begin, date_end))

        for sensor in cursor:
            measures.append(sensor)

    except Exception as e:
        print(f"Error when getting measures of greenhouse {greenhouse_serial}: {e}")

    return measures


def get_sensor_unit(sensor_id):
    db = get_db()
    cursor = db.cursor()
    sensor_type = get_sensor_type(sensor_id)

    if sensor_type == "temperature":
        return "°C"
    elif "humidity" in sensor_type:
        return "%"
    elif sensor_type == "ligth":
        return "lux"
    elif sensor_type == "O2":
        return "ppm"
    elif sensor_type == "water_level":
        return "cm"
