from src.database.database import get_db
from src.database.plant import get_name_plant
from datetime import datetime, timedelta


def check_greenhouse_owner(user_name, greenhouse_serial):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT user_name "
            "FROM UserGreenHouses "
            "WHERE user_name= %s AND greenhouse_serial = %s",
            (user_name, greenhouse_serial)
        )
        user_name = cursor.fetchone()
        if user_name is None:
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
            "SELECT greenhouse_serial, name "
            "FROM UserGreenHouses "
            "WHERE user_name = %s",
            (user_name,)
        )
        for (serial, greenhouse_name) in cursor:
            greenhouses[serial] = greenhouse_name

        return greenhouses

    except Exception as e:
        print(f"Error when getting greenhouses: {e}")


def get_greenhouse_name(serial_number, user_name):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT name "
            "FROM UserGreenHouses "
            "WHERE greenhouse_serial = %s and user_name = %s ",
            (serial_number, user_name)
        )
        name = cursor.fetchone()
        if name is None:
            return None
        return name[0]

    except Exception as e:
        print(f"Error when getting greenhouse name: {e}")
        return None


def get_greenhouse_targets(greenhouse_serial):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT temperature, soil_humidity, air_humidity, light "
            "FROM GreenHouses "
            "WHERE serial = %s",
            (greenhouse_serial,)
        )
        data_targets = cursor.fetchone()
        for key in data_targets:
            if key != "light":
                data_targets[key] = data_targets[key] / 10
        return data_targets

    except Exception as e:
        print(f"Error when getting greenhouse targets: {e}")

    return {}


def get_greenhouse_actuator(greenhouse_serial):
    db = get_db()
    cursor = db.cursor()
    owner = None
    collaborators = []
    guests = []

    try:
        cursor.execute(
            "SELECT user_name, role "
            "FROM UserGreenHouses WHERE greenhouse_serial = %s",
            (greenhouse_serial,)
        )
        for (user_name, role) in cursor:
            if role == "owner":
                owner = user_name
            elif role == "collaborator":
                collaborators.append(user_name)
            else:
                guests.append(user_name)

    except Exception as e:
        print(f"Error when getting list users greenhouse: {e}")

    return owner, collaborators, guests


def get_greenhouse_is_custom_config(greenhouse_serial):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT is_custom_config "
            "FROM GreenHouses "
            "WHERE serial = %s",
            (greenhouse_serial,)
        )
        return cursor.fetchone()[0]

    except Exception as e:
        print(f"Error when getting greenhouse config: {e}")

    return False


def get_role_user(greenhouse_serial, user_name):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT role "
            "FROM UserGreenHouses "
            "WHERE user_name = %s AND greenhouse_serial = %s",
            (user_name, greenhouse_serial)
        )
        role = cursor.fetchone()
        if role is None:
            return None
        return role[0]

    except Exception as e:
        print(f"Error when getting role user: {e}")
        return None


def set_role_user(greenhouse_serial, username, role):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "UPDATE UserGreenHouses "
            "SET role = %s "
            "WHERE user_name = %s AND greenhouse_serial = %s",
            (role, username, greenhouse_serial)
        )
        db.commit()

    except Exception as e:
        print(f"Error when setting user role: {e}")
        return False

    return True


def set_custom_config_greenhouse(greenhouse_serial, temperature, soil_humidity, air_humidity, light):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "UPDATE GreenHouses "
            "SET temperature = %s, soil_humidity = %s, air_humidity = %s, light = %s, is_custom_config = 1 "
            "WHERE serial = %s",
            (float(temperature)*10, float(soil_humidity)*10, float(air_humidity)*10, int(light), greenhouse_serial)
        )
        db.commit()

    except Exception as e:
        print(f"Error when setting custom config: {e}")
        return False

    return True


def create_notification_measures(greenhouse_serial):
    db = get_db()
    cursor = db.cursor()
    targets = get_greenhouse_targets(greenhouse_serial)
    max_delta = max_delta_values()
    sensors = get_sensors_greenhouse(greenhouse_serial)
    latest_measures = get_latest_mesures(sensors)
    print(latest_measures)
    try:
        for sensor_id, sensor_type in sensors.items():
            if sensor_type != "water_level" and sensor_type != "O2":
                date_latest_notification = get_date_latest_notification(greenhouse_serial, sensor_type)
                if (latest_measures[sensor_id]['value'] > targets[sensor_type] + max_delta[sensor_type] and
                        (date_latest_notification is None or date_latest_notification < datetime.now() -
                         timedelta(hours=2))):
                    if sensor_type == "temperature":
                        cursor.execute(
                            "INSERT INTO Notifications (greenhouse_serial, message, notification_type) "
                            "VALUES (%s, %s, %s) ",
                            (greenhouse_serial, "La température est trop élevée", sensor_type)
                        )
                        db.commit()
                    elif sensor_type == "soil_humidity":
                        cursor.execute(
                            "INSERT INTO Notifications (greenhouse_serial, message, notification_type) "
                            "VALUES (%s, %s, %s) ",
                            (greenhouse_serial, "L'humidité du sol est trop élevée", sensor_type)
                        )
                        db.commit()
                    elif sensor_type == "air_humidity":
                        cursor.execute(
                            "INSERT INTO Notifications (greenhouse_serial, message, notification_type) "
                            "VALUES (%s, %s, %s) ",
                            (greenhouse_serial, "L'humidité de l'air est trop élevée", sensor_type)
                        )
                        db.commit()
                    elif sensor_type == "light":
                        cursor.execute(
                            "INSERT INTO Notifications (greenhouse_serial, message, notification_type) "
                            "VALUES (%s, %s, %s) ",
                            (greenhouse_serial, "La lumière est trop élevée", sensor_type)
                        )
                        db.commit()

                elif (latest_measures[sensor_id]['value'] < targets[sensor_type] + max_delta[sensor_type] and
                      (date_latest_notification is None or date_latest_notification < datetime.now() -
                       timedelta(hours=2))):
                    if sensor_type == "temperature":
                        cursor.execute(
                            "INSERT INTO Notifications (greenhouse_serial, message, notification_type) "
                            "VALUES (%s, %s, %s) ",
                            (greenhouse_serial, "La température est trop basse", sensor_type)
                        )
                        db.commit()
                    elif sensor_type == "soil_humidity":
                        cursor.execute(
                            "INSERT INTO Notifications (greenhouse_serial, message, notification_type) "
                            "VALUES (%s, %s, %s) ",
                            (greenhouse_serial, "L'humidité du sol est trop basse", sensor_type)
                        )
                        db.commit()
                    elif sensor_type == "air_humidity":
                        cursor.execute(
                            "INSERT INTO Notifications (greenhouse_serial, message, notification_type) "
                            "VALUES (%s, %s, %s) ",
                            (greenhouse_serial, "L'humidité de l'air est trop basse", sensor_type)
                        )
                        db.commit()
                    elif sensor_type == "light":
                        cursor.execute(
                            "INSERT INTO Notifications (greenhouse_serial, message, notification_type) "
                            "VALUES (%s, %s, %s) ",
                            (greenhouse_serial, "La luminosité est trop basse", sensor_type)
                        )
                        db.commit()

    except Exception as e:
        print(f"Error when creating notification for greenhouse {greenhouse_serial}: {e}")


def get_greenhouse_notification_date(greenhouse_serial):
    db = get_db()
    cursor = db.cursor()
    messages = {}

    try:
        cursor.execute(
            "SELECT id, message, date "
            "FROM Notifications "
            "WHERE greenhouse_serial = %s "
            "ORDER BY date DESC ",
            (greenhouse_serial,)
        )
        for (id_message, message, date) in cursor:
            messages[id_message] = (message, date)
        return messages

    except Exception as e:
        print(f"Error when getting greenhouse notification: {e}")

    return False


def get_latest_mesures(sensors):
    db = get_db()
    cursor = db.cursor()
    measures = {}

    try:
        for sensor_id, sensor_type in sensors.items():
            cursor.execute(
                "SELECT value, date "
                "FROM Measures "
                "WHERE sensor_id = %s "
                "ORDER BY date DESC "
                "LIMIT 1",
                (sensor_id,)
            )
            result = cursor.fetchone()
            if result is not None:
                if sensor_type != "light":
                    measures[sensor_id] = {'value': result[0], 'date': result[1], 'type': sensor_type}
                else:
                    measures[sensor_id] = {'value': result[0]/10, 'date': result[1], 'type': sensor_type}

    except Exception as e:
        print(f"Error when getting latest measures: {e}")

    return measures


def max_delta_values():
    temperature = 5
    soil_humidity = 10
    air_humidity = 10
    light = 1000
    return {'temperature': temperature, 'soil_humidity': soil_humidity, 'air_humidity': air_humidity, 'light': light}


def get_sensors_greenhouse(greenhouse_serial):
    db = get_db()
    cursor = db.cursor()
    sensors = {}

    try:
        cursor.execute(
            "SELECT id, type "
            "FROM Sensors "
            "WHERE greenhouse_serial = %s",
            (greenhouse_serial,)
        )
        for (sensor_id, sensor_type) in cursor:
            sensors[sensor_id] = sensor_type

        return sensors

    except Exception as e:
        print(f"Error when getting sensors: {e}")

    return False


def get_date_latest_notification(greenhouse_serial, type_notification):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT date "
            "FROM Notifications "
            "WHERE greenhouse_serial = %s and notification_type = %s "
            "ORDER BY date DESC "
            "LIMIT 1",
            (greenhouse_serial, type_notification)
        )
        date = cursor.fetchone()
        if date is None:
            return None
        return date[0]

    except Exception as e:
        print(f"Error when getting date latest notification: {e}")

    return None


def create_notification_new_user(greenhouse_serial, user_name):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO Notifications (greenhouse_serial, message, notification_type) "
            "VALUES (%s, %s, %s) ",
            (greenhouse_serial, f"Nouvel utilisateur: {user_name}", "new_member")
        )
        db.commit()

    except Exception as e:
        print(f"Error when creating notification for new user: {e}")


def get_plant_via_association(association_id):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT plant_id "
            "FROM GreenHousePlants "
            "WHERE id = %s ",
            (association_id,)
        )
        plant, = cursor.fetchone()
        if plant is None:
            return None
        return plant

    except Exception as e:
        print(f"Error when getting plant via association: {e}")
        return None


def create_notification_plant(greenhouse_serial, plant_id, count, type_action):
    db = get_db()
    cursor = db.cursor()

    try:
        if type_action == "add":
            cursor.execute(
                "INSERT INTO Notifications (greenhouse_serial, message, notification_type) "
                "VALUES (%s, %s, %s) ",
                (greenhouse_serial, f"Ajout de {count} {get_name_plant(plant_id)}(s)", "new_plant")
            )
            db.commit()
        else:
            cursor.execute(
                "INSERT INTO Notifications (greenhouse_serial, message, notification_type) "
                "VALUES (%s, %s, %s) ",
                (greenhouse_serial, f"Suppression de {get_name_plant(get_plant_via_association(plant_id))}",
                 "drop_plant")
            )
            db.commit()

    except Exception as e:
        print(f"Error when creating notification for new plant: {e}")


def create_notification_custom_config(greenhouse_serial, username):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO Notifications (greenhouse_serial, message, notification_type) "
            "VALUES (%s, %s, %s) ",
            (greenhouse_serial, f"{username} a modifié personnalisé les valeurs cibles", "custom_config")
        )
        db.commit()

    except Exception as e:
        print(f"Error when creating custom notification: {e}")
