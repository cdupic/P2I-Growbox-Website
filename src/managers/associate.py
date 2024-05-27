from flask import session, redirect, url_for, request

from src.database.database import get_db



def associate_manager(greenhouse_serial):
    if verify_greenhouse_exists_and_not_linked(request.form['ghs']):
        link_greenhouse_to_user(request.form['ghs'], session['user_name'], session['ghn'])
        return redirect(url_for('greenhouses_page'))


def verify_greenhouse_exists_and_not_linked(serial_number):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT serial "
            "FROM GreenHouses "
            "WHERE serial = %s and user_name is NULL",
            (serial_number,)
        )
        serial = cursor.fetchone()
        if serial is None:
            return False
        return True

    except Exception as e:
        print(f"Error when verifying greenhouse exists: {e}")
        return False


def link_greenhouse_to_user(greenhouse_serial, user_name, greenhouse_name):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "UPDATE GreenHouses SET user_name = %s, name = %s WHERE serial = %s",
            (user_name, greenhouse_name, greenhouse_serial)
        )
        db.commit()

    except Exception as e:
        print(f"Error when linking greenhouse to user: {e}")
        return False

    return True

