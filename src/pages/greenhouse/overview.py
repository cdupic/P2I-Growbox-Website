from flask import render_template, redirect, url_for, session

from src.database.greenhouse import check_greenhouse_owner, get_greenhouse_name
from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse, get_data_sensors_since, \
    get_data_actuators_since
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
    data_actuators = get_data_actuators_since(greenhouse_serial, [], session['graphs_days'])

    return render_template('pages/greenhouse_overview.j2',
                           greenhouse_serial=greenhouse_serial,
                           sensors=sensors.items(),
                           actuators=actuators.items(),
                           data_sensors=data_sensors,
                           greenhouse_name=get_greenhouse_name(greenhouse_serial))
