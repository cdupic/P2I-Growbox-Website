from flask import session, redirect, url_for, request, render_template

from src.database.database import get_db
from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse, get_data_sensors_since



def associate_manager():
    if verify_greenhouse_exists(request.args.get('ghs')):
        link_greenhouse_to_user(request.args.get('ghs'), session['user_name'], request.args.get('ghn'))
        session['success'] = 'Serre liée à votre profil !'
        # return render_template('pages/greenhouse_overview.j2',
        #                        greenhouse_serial=request.args.get('ghs'),
        #                        sensors=get_sensors_greenhouse(request.args.get('ghs')).items(),
        #                        actuators=get_actuators_greenhouse(request.args.get('ghs')).items(),
        #                        data_sensors=get_data_sensors_since(request.args.get('ghs'), [], session['graphs_days']),
        #                        current_sidebar_item=('overview', None),
        #                        greenhouse_name=request.args.get('ghn'))
    else:
        session['error'] = "Numéro de série invalide ou serre deja liée à un compte."

    return redirect(url_for('greenhouses_page'))


def verify_greenhouse_exists(serial_number):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT serial "
            "FROM GreenHouses "
            "WHERE serial = %s ",
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
    print(greenhouse_serial, user_name, greenhouse_name)
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "UPDATE GreenHouses SET name = %s WHERE serial = %s",
            (greenhouse_name, greenhouse_serial)
        )
        db.commit()
        cursor.execute(
            " INSERT INTO UserGreenHouses (user_name, greenhouse_serial) VALUES(%s, %s) ",
            (user_name, greenhouse_serial)
        )
        db.commit()

    except Exception as e:
        print(f"Error when linking greenhouse to user: {e}")
        return False

    return True

