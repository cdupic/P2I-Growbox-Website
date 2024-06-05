from datetime import datetime, timedelta, time

from flask import g, session

from src.database.database import get_db
from src.utils.sensor_names import convert_actuator_type_to_french
from src.utils.sensor_names import convert_sensor_type_to_french


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


def get_data_sensors_since(serial_number, sensors_list, day_start, day_end):
    db = get_db()
    cursor = db.cursor()
    data = {}
    if not sensors_list:
        sensors_list = tuple(get_sensors_greenhouse(serial_number).keys())
    sensors_list_str = ', '.join(map(str, sensors_list))
    try:
        cursor.execute(
            "SELECT Sensors.type,  Measures.date, Measures.value "
            "FROM Sensors, GreenHouses, Measures "
            "WHERE greenhouse_serial = %s and GreenHouses.serial = Sensors.greenhouse_serial "
            "and Sensors.id = Measures.sensor_id and Sensors.id in (%s) "
            "and (Measures.date) BETWEEN (%s) and (%s)",
            (serial_number, sensors_list_str, day_start, day_end)
        )
        for (sensor_type, date, value) in cursor:
            if sensor_type not in data:
                data[sensor_type] = {}
            if sensor_type != "light":
                data[sensor_type][date] = value / 10
            elif sensor_type == "light":
                data[sensor_type][date] = value

        return data

    except Exception as e:
        print(f"Error when getting data: {e}")


def get_data_actuators_since(greenhouse_serial, actuators_list, day_start, day_end):
    db = get_db()
    cursor = db.cursor()
    data = {}
    if not actuators_list:
        actuators_list = tuple(get_actuators_greenhouse(greenhouse_serial).keys())
    actuators_list_str = ', '.join(map(str, actuators_list))

    try:
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


def get_actuator_unit(actuator_type):
    if actuator_type == "water_level":
        return "mm"



def get_greenhouse_actions(greenhouse_serial, actuator_id, date_start, date_end):
    cursor = g.db.connect().cursor()

    try:
        cursor.execute(
            "SELECT Actions.actuator_id, Actions.date, Actions.value, Actuators.type "
            "FROM Actions, Actuators "
            "WHERE Actions.actuator_id = Actuators.id and Actuators.id= %s and Actuators.greenhouse_serial = %s and "
            "Actions.date BETWEEN %s and %s "
            "ORDER BY Actions.date",
            (actuator_id, greenhouse_serial, date_start, date_end))

        for (actuator_id, date, value, sensor_type) in cursor:
            print(f"Action in {greenhouse_serial} the {date}, done by actuator {actuator_id}, {sensor_type} : {value}")

    except Exception as e:
        print(f"Error when getting actions of greenhouse : {greenhouse_serial}: {e}")


def get_greenhouse_measures(greenhouse_serial, sensor_id, date_start, date_end):
    cursor = g.db.cursor
    measures = []

    try:
        cursor.execute(
            "SELECT Measures.sensor_id, Measures.date, Measures.value, Sensors.type "
            "FROM Measures, Sensors "
            "WHERE Measures.sensor_id = Sensors.id  and Sensors.id = %s and Sensors.greenhouse_serial= %s and "
            "Measures.date BETWEEN %s and %s ",
            (sensor_id, greenhouse_serial, date_start, date_end))

        for sensor in cursor:
            measures.append(sensor)

    except Exception as e:
        print(f"Error when getting measures of greenhouse {greenhouse_serial}: {e}")

    return measures


def get_sensor_unit(sensor_type):
    if sensor_type == "temperature":
        return "°C"
    elif "humidity" in sensor_type:
        return "%"
    elif sensor_type == "light":
        return "lux"
    elif sensor_type == "O2":
        return "ppm"
    elif sensor_type == "water_level":
        return "cm"


def get_number_of_measures(greenhouse_serial, list_sensors):
    db = get_db()
    cursor = db.cursor()
    try:
        if not list_sensors:
            list_sensors = tuple(get_sensors_greenhouse(greenhouse_serial).keys())
        sensors_list_str = ', '.join(map(str, list_sensors))

        number_measures = 0

        for sensor_id in sensors_list_str:
            cursor.execute(
                "SELECT count(*) "
                "FROM Sensors, Measures "
                "WHERE Sensors.greenhouse_serial = %s and Sensors.id = Measures.sensor_id and Sensors.id=%s ",
                (greenhouse_serial, sensor_id)
            )
            number_measures += cursor.fetchone()[0]
        return number_measures

    except Exception as e:
        print(f"Error when getting number of measures of sensor {list_sensors} in greenhouse {greenhouse_serial}: {e}")
        return None


def get_number_of_actions(greenhouse_serial, actuator_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT COUNT(*) "
            "FROM Actions, Actuators "
            "WHERE Actions.actuator_id = Actuators.id and Actuators.id = %s and Actuators.greenhouse_serial= %s ",
            (actuator_id, greenhouse_serial))

        return cursor.fetchone()[0]

    except Exception as e:
        print(f"Error when getting number of actions of actuator {actuator_id} in greenhouse {greenhouse_serial}: {e}")
        return None


def get_date_last_measure(greenhouse_serial, sensor_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT MAX(Measures.date) "
            "FROM Measures, Sensors "
            "WHERE Measures.sensor_id = Sensors.id and Sensors.id = %s and Sensors.greenhouse_serial= %s ",
            (sensor_id, greenhouse_serial))

        return cursor.fetchone()[0]

    except Exception as e:
        print(f"Error when getting last measure of sensor {sensor_id} in greenhouse {greenhouse_serial}: {e}")
        return None


def get_number_measures(greenhouse_serial, date_start=None, date_end=None):
    db = get_db()
    cursor = db.cursor()
    try:
        if not date_start:
            cursor.execute(
                "SELECT count(*) "
                "FROM Sensors, Measures "
                "WHERE Sensors.greenhouse_serial = %s and Sensors.id = Measures.sensor_id",
                (greenhouse_serial,)
            )
            return cursor.fetchone()[0]
        else:
            cursor.execute(
                "SELECT count(*) "
                "FROM Sensors, Measures "
                "WHERE Sensors.greenhouse_serial = %s and Sensors.id = Measures.sensor_id"
                " and (Measures.date) BETWEEN %s and %s",
                (greenhouse_serial, date_start, date_end)
            )
            return cursor.fetchone()[0]


    except Exception as e:
        print(f"Error when getting number of measures in greenhouse {greenhouse_serial}: {e}")
        return None


def get_date_end_start():
    if session.get('graph_start_date') and session.get('graph_end_date'):
        return session['graph_start_date'], session['graph_end_date']

    else:
        if not session.get('graph_delta_time') and session.get('graph_delta_time') != 0:
            session['graph_delta_time'] = 7
        return (datetime.combine(datetime.utcnow(), time(0, 0, 0)) -
                timedelta(days=session['graph_delta_time'])), datetime.utcnow()


def get_data_all_sensors(greenhouse_serial, date_start, date_end):
    db = get_db()
    cursor = db.cursor()
    data = {}
    try:
        cursor.execute(
            "SELECT Sensors.id, Sensors.type, Measures.date, Measures.value "
            "FROM Sensors, Measures "
            "WHERE Sensors.greenhouse_serial = %s "
            "and Sensors.id = Measures.sensor_id and (Measures.date) BETWEEN %s and %s",
            (greenhouse_serial, date_start, date_end)
        )
        for (sensor_id, sensor_type, date, value) in cursor:
            if sensor_id not in data:
                data[sensor_id] = [[], [], []]
                data[sensor_id][2] = sensor_type
            if sensor_type != "light":
                data[sensor_id][0].append(value / 10)
            elif sensor_type == "light":
                data[sensor_id][0].append(value)
            data[sensor_id][1].append(date)
        return data

    except Exception as e:
        print(f"Error when getting data: {e}")
        return None


def get_date_latest_measure(greenhouse_serial):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT MAX(Measures.date) "
            "FROM Sensors, Measures "
            "WHERE Sensors.greenhouse_serial = %s and Sensors.id = Measures.sensor_id ",
            (greenhouse_serial,)
        )
        return cursor.fetchone()[0]

    except Exception as e:
        print(f"Error when getting latest measure of greenhouse {greenhouse_serial}: {e}")
        return None


def get_format_latest_measure(date_latest):
    diff = datetime.utcnow() - date_latest
    if diff < timedelta(minutes=1):
        return f"il y a {diff.seconds} seconde{'' if diff.seconds == 1 else 's'}"
    elif diff < timedelta(hours=1):
        return f"il y a {diff.seconds // 60} minute{'' if diff.seconds // 60 == 1 else 's'}"
    elif diff < timedelta(days=1):
        return f"il y a {diff.seconds // 3600} heure{'' if diff.seconds // 3600 == 1 else 's'}"
    else:
        return f"le {date_latest.strftime('%d/%m/%Y à %H:%M')}"

