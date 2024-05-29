from src.database.database import get_db


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
    targets = {}

    try:
        cursor.execute(
            "SELECT temperature, soil_humidity, air_humidity, light, O2 "
            "FROM GreenHouses "
            "WHERE serial = %s",
            (greenhouse_serial,)
        )
        for (data) in cursor:
            targets = data

        return targets

    except Exception as e:
        print(f"Error when getting greenhouse targets: {e}")



