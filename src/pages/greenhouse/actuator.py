from datetime import datetime, timedelta

import pytz
from flask import redirect, url_for, render_template

from src.database.greenhouse import get_dic_users_role_greenhouse
from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse, get_data_actuators_since, \
    get_actuator_type, get_actuator_unit, get_number_of_actions, get_date_end_start, get_format_latest_measure
from src.utils.sensor_names import convert_actuator_type_to_full_name
from src.utils.user import is_user_authenticated


def greenhouse_actuator_page(greenhouse_serial, actuator_id):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))

    sensors = get_sensors_greenhouse(greenhouse_serial)
    actuators = get_actuators_greenhouse(greenhouse_serial)

    users_roles = get_dic_users_role_greenhouse(greenhouse_serial)
    actuator_type = get_actuator_type(actuator_id)
    actions = {}

    date_start, date_end = get_date_end_start()

    date_latest = datetime.utcnow() - timedelta(days=365)

    for data in get_data_actuators_since(greenhouse_serial, [actuator_id], date_start, date_end).values():
        for date, value in data.items():
            if date > date_latest:
                date_latest = date
            actions[date] = value

    if actions != {}:
        date_latest = get_format_latest_measure(date_latest)
    else:
        date_latest = None

    return render_template('pages/greenhouse_actuator.j2',
                           greenhouse_serial=greenhouse_serial,
                           sidebar_sensors=sensors.items(),
                           sidebar_actuators=actuators.items(),
                           sidebar_users=users_roles.items(),
                           ratio_measures=str(len(actions)) + ' sur ' + str(
                               get_number_of_actions(greenhouse_serial, actuator_id)),
                           date_latest=date_latest,
                           actions=actions,
                           actuator_id=actuator_id,
                           actuator_type=actuator_type,
                           current_actuator_full_name=convert_actuator_type_to_full_name(actuator_type),
                           actuator_unit=get_actuator_unit(actuator_id),
                           current_sidebar_item=('actuator', int(actuator_id)),
                           from_datetime_utc=str(date_start),
                           to_datetime_utc=str(date_end),
                           from_date=date_start.astimezone(pytz.timezone('Europe/Paris')).strftime("%Y-%m-%d"),
                           to_date=date_end.astimezone(pytz.timezone('Europe/Paris')).strftime("%Y-%m-%d"))
