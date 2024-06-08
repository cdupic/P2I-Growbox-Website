from flask import session, redirect, url_for, request

from src.database.database import get_db
from src.database.greenhouse import create_new_user_notification


def associate_manager():
    if verify_greenhouse_exists_and_not_linked(request.args.get('ghs'), session['user_name']):
        link_greenhouse_to_user(request.args.get('ghs'), session['user_name'], request.args.get('ghn'))
        session['success'] = 'Serre liée à votre profil !'
        create_new_user_notification(request.args.get('ghs'), session['user_name'])
        # return render_template('pages/greenhouse_overview.j2',
        #                        greenhouse_serial=request.args.get('ghs'),
        #                        sensors=get_sensors_greenhouse(request.args.get('ghs')).items(),
        #                        actuators=get_actuators_greenhouse(request.args.get('ghs')).items(),
        #                        data_sensors=get_data_sensors_since(request.args.get('ghs'), [], session['graphs_days']),
        #                        current_sidebar_item=('overview', None),
        #                        greenhouse_name=request.args.get('ghn'))
    else:
        session['error'] = "Numéro de série invalide ou serre deja liée à vous."

    return redirect(url_for('greenhouses_page'))


def verify_greenhouse_exists_and_not_linked(serial_number, session_user_name):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT greenhouse_serial FROM UserGreenHouses "
            "WHERE greenhouse_serial = %s AND user_name = %s",
            (serial_number, session_user_name),
        )
        serial = cursor.fetchone()
        if serial is None:
            return True
        return False

    except Exception as e:
        print(f"Error when verifying greenhouse exists: {e}")
        return False


def link_greenhouse_to_user(greenhouse_serial, user_name, greenhouse_name):
    db = get_db()
    cursor = db.cursor()

    try:
        if greenhouse_already_linked(greenhouse_serial):
            role = "guest"
        else:
            role = "owner"
        cursor.execute(
            " INSERT INTO UserGreenHouses (user_name, greenhouse_serial, name, role) VALUES(%s, %s, %s, %s) ",
            (user_name, greenhouse_serial, greenhouse_name, role),
        )
        db.commit()

    except Exception as e:
        print(f"Error when linking greenhouse to user: {e}")
        return False

    return True


def greenhouse_already_linked(greenhouse_serial):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT greenhouse_serial FROM UserGreenHouses "
            "WHERE greenhouse_serial = %s",
            (greenhouse_serial,),
        )
        serial = cursor.fetchone()
        if serial is None:
            return False
        return True

    except Exception as e:
        print(f"Error when verifying greenhouse exists: {e}")
        return False
