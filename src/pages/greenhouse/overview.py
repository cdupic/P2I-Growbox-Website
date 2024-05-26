from flask import render_template, redirect, url_for, session

from src.database.sql_utils import check_greenhouse_owner, get_sensors_greenhouse, get_actuators_greenhouse, \
    get_data_sensors_since, get_data_actuators_since
from src.utils.user import is_user_authenticated


def greenhouse_overview_page(greenhouse_serial):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))

    if not check_greenhouse_owner(session['user_name'], greenhouse_serial):
        session['error'] = f"La serre {greenhouse_serial} n'existe pas ou n'est pas accessible avec votre compte."
        return redirect(url_for('greenhouses_page'))

    sensors = get_sensors_greenhouse(greenhouse_serial)
    actuators = get_actuators_greenhouse(greenhouse_serial)

    data_sensors = get_data_sensors_since(greenhouse_serial, [], session['graphs_days'])
    # TODO: get data of all actuators the same way the data of sensors is fetched.
    data_actuators = get_data_actuators_since(greenhouse_serial, [], session['graphs_days'])

    return render_template('pages/greenhouse_overview.j2',
                           force_sidebar=True,
                           greenhouse_serial=greenhouse_serial,
                           sensors=sensors,
                           actuators=actuators,
                           data_sensors=data_sensors)
