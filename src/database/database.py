import os
from datetime import datetime, timedelta

import mysql.connector
from dbutils.pooled_db import PooledDB
from dotenv import load_dotenv
from flask import g

load_dotenv()

pool = PooledDB(
    creator=mysql.connector,
    maxconnections=10,
    mincached=2,
    maxcached=5,
    blocking=True,
    host=os.getenv("SQL_HOST"),
    user=os.getenv("SQL_USER"),
    password=os.getenv("SQL_PASSWORD"),
    database=os.getenv("SQL_DATABASE"),
    port=3306
)


def get_db():
    try:
        return pool.connection()
    except Exception as e:
        print("[ERROR] MySQL: " + str(e))


def init_db():
    if 'db' not in g:
        g.db = get_db()


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()


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
            "SELECT name "
            "FROM GreenHouses "
            "WHERE user_name = %s",
            (user_name,)
        )
        for (greenhouse_name,) in cursor:
            greenhouses['name'] = greenhouse_name

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


def get_data_sensors_since(serial_number, days):
    db = get_db()
    cursor = db.cursor()
    data = {}

    try:
        cursor.execute(
            "SELECT Sensors.id,  Measures.date, Measures.value "
            "FROM Sensors, GreenHouses, Measures "
            "WHERE greenhouse_serial = %s and GreenHouses.serial = Sensors.greenhouse_serial "
            "and Sensors.id = Measures.sensor_id and (Measures.date) > %s",
            (serial_number, datetime.now() - timedelta(days=days))
        )
        for (sensor_id, date, value) in cursor:
            if sensor_id not in data:
                data[sensor_id] = {}
            data[sensor_id][date] = value

        return data

    except Exception as e:
        print(f"Error when getting data: {e}")
