from flask import render_template, redirect, url_for, session
from datetime import datetime, timedelta, time
import pytz

from src.database.greenhouse import check_greenhouse_owner, get_greenhouse_name, get_dic_users_role_greenhouse
from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse, get_data_sensors_since, \
    get_data_actuators_since, get_number_measures
from src.utils.user import is_user_authenticated


def greenhouse_overview_page(greenhouse_serial):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))
    if not check_greenhouse_owner(session['user_name'], greenhouse_serial):
        session['error'] = f"La serre {greenhouse_serial} n'existe pas ou n'est pas accessible avec votre compte."
        return redirect(url_for('greenhouses_page'))

    sensors = get_sensors_greenhouse(greenhouse_serial)
    actuators = get_actuators_greenhouse(greenhouse_serial)

    users_roles = get_dic_users_role_greenhouse(greenhouse_serial)

    session['serial'] = greenhouse_serial

    if session.get('graph_start_date') and session.get('graph_start_date'):
        date_start = session['graph_start_date']
        date_end = session['graph_end_date']

    else:
        if not session.get('graph_delta_time'):
            session['graph_delta_time'] = 7

        date_start = datetime.utcnow() - timedelta(days=session['graph_delta_time'])
        date_end = datetime.utcnow()

    data_sensors = get_data_sensors_since(greenhouse_serial, [], date_start, date_end)
    data_actuators = get_data_actuators_since(greenhouse_serial, [], date_start, date_end)


    if session.get('graph_start_date') and session.get('graph_end_date'):
        date_start = session['graph_start_date']
        date_end = session['graph_end_date']

    else:
        if not session.get('graph_delta_time'):
            session['graph_delta_time'] = 7
        date_start = datetime.utcnow() - timedelta(days=session['graph_delta_time'])
        date_end = datetime.utcnow()

    return render_template('pages/greenhouse_overview.j2',
                           greenhouse_serial=greenhouse_serial,
                           sidebar_sensors=sensors.items(),
                           sidebar_actuators=actuators.items(),
                           sidebar_users=users_roles.items(),
                           number_mesures=str(get_number_measures(greenhouse_serial, date_start, date_end)) + ' sur ' +
                           str(get_number_measures(greenhouse_serial, [])),
                           current_sidebar_item=('overview', None),
                           data_sensors=data_sensors,
                           greenhouse_name=get_greenhouse_name(greenhouse_serial, session['user_name']))
