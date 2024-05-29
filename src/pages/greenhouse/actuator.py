from flask import redirect, url_for, session, render_template

from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse, get_data_actuators_since, \
    get_actuator_type
from src.database.greenhouse import get_dic_users_role_greenhouse

from src.utils.measure import convert_actuator_type_to_french
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
    for data in get_data_actuators_since(greenhouse_serial, [actuator_id], session['graphs_days']).values():
        for date, value in data.items():
            actions[date] = value

    return render_template('pages/greenhouse_actuator.j2',
                           actions=actions,
                           actuator_type=actuator_type_french,
                           greenhouse_serial=greenhouse_serial,
                           sidebar_sensors=sensors.items(),
                           current_sidebar_item=('actuator', int(actuator_id)),
                           sidebar_actuators=actuators.items())
