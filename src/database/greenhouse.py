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


def switch_greenhouse_custom_config(greenhouse_serial):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "UPDATE GreenHouses "
            "SET is_custom_config = 1 "
            "WHERE serial = %s",
            (greenhouse_serial,)
        )
        db.commit()

    except Exception as e:
        print(f"Error when switching greenhouse custom config: {e}")


def get_config_greenhouse(greenhouse_serial):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT is_custom_config "
            "FROM GreenHouses "
            "WHERE serial = %s",
            (greenhouse_serial,)
        )
        return cursor.fetchone()

    except Exception as e:
        print(f"Error when getting greenhouse config: {e}")

    return {}

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


