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
    sensors = []

    try:
        cursor.execute(
            "SELECT Sensors.id, Sensors.type, GreenHouses.name "
            "FROM Sensors, GreenHouses "
            "WHERE greenhouse_serial = %s and GreenHouses.serial = Sensors.greenhouse_serial ",
            (greenhouse_serial,)
        )

        for (ID, sensor_type, name) in cursor:
            if name not in sensors:
                sensors.append(name)
            sensors.append([{ID : sensor_type}])


        return sensors

    except Exception as e:
        print(f"Error when getting sensors: {e}")


def get_actuators_greenhouse(greenhouse_serial):
    db = get_db()
    cursor = db.cursor()
    actuators = []

    try:
        cursor.execute(
            "SELECT Actuators.id, Actuators.type, GreenHouses.name "
            "FROM Actuators, GreenHouses "
            "WHERE greenhouse_serial = %s and GreenHouses.serial = Actuators.greenhouse_serial ",
            (greenhouse_serial,)
        )

        for (ID, actuator_type, name) in cursor:
            if name not in actuators:
                actuators.append(name)
            actuators.append([{ID : actuator_type}])


        return actuators

    except Exception as e:
        print(f"Error when getting actuators: {e}")


def get_data_sensors_since(serial_number, days):
    db = get_db()
    cursor = db.cursor()
    data = {}

    try:
        cursor.execute(
            "SELECT Sensors.id, Sensors.type, GreenHouses.name, Measures.value, Measures.date "
            "FROM Sensors, GreenHouses, Measures "
            "WHERE greenhouse_serial = %s and GreenHouses.serial = Sensors.greenhouse_serial "
            "and Sensors.id = Measures.sensor_id and (Measures.date) > %s" ,
            (serial_number, datetime.now() - timedelta(days=days))
        )
        for (ID, sensor_type, name, value, date) in cursor:
            if name not in data:
                data[name] = {}
            if ID not in data[name]:
                data[name][ID] = []

            data[name][ID].append([value, date])

        return data

    except Exception as e:
        print(f"Error when getting data: {e}")

