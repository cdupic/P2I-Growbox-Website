from flask import redirect, url_for, session, render_template
from datetime import datetime, timedelta

from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse, get_data_actuators_since, \
    get_actuator_type
from src.database.greenhouse import get_dic_users_role_greenhouse

from src.utils.sensor_names import convert_actuator_type_to_french
from src.utils.user import is_user_authenticated


def greenhouse_actuator_page(greenhouse_serial, actuator_id):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))

    actuator_type = get_actuator_type(actuator_id)
    actuator_type_french = convert_actuator_type_to_french(actuator_type)

    sensors = get_sensors_greenhouse(greenhouse_serial)
    actuators = get_actuators_greenhouse(greenhouse_serial)

    users_roles = get_dic_users_role_greenhouse(greenhouse_serial)

    actions = {}

    if session.get('graph_start_date'):
        date_start = session['graph_start_date']
        date_end = session['graph_end_date']

    else:
        if not session.get('graph_delta_time'):
            session['graph_delta_time'] = 7

        date_start = datetime.utcnow() - timedelta(days=session['graph_delta_time'])
        date_end = datetime.utcnow()

    for data in get_data_actuators_since(greenhouse_serial, [actuator_id], date_start, date_end).values():
        for date, value in data.items():
            actions[date] = value


    return render_template('pages/greenhouse_actuator.j2',
                           actions=actions,
                           actuator_type=actuator_type_french,
                           greenhouse_serial=greenhouse_serial,
                           sidebar_sensors=sensors.items(),
                           current_sidebar_item=('actuator', int(actuator_id)),
                           sidebar_actuators=actuators.items())
