from datetime import datetime, timedelta

from flask import render_template, redirect, url_for, session

from src.database.greenhouse import get_greenhouse_targets, get_dic_users_role_greenhouse
from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse, get_data_sensors_since, \
    get_sensor_type, get_sensor_unit, get_number_of_measures
from src.utils.sensor_names import convert_sensor_type_to_french, convert_sensor_type_to_full_name
from src.utils.user import is_user_authenticated


def greenhouse_sensor_page(greenhouse_serial, sensor_id):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))

    sensor_type = get_sensor_type(sensor_id)
    sensor_type_french = convert_sensor_type_to_french(sensor_type)
    sensor_unit = get_sensor_unit(sensor_id)

    sensors = get_sensors_greenhouse(greenhouse_serial)
    actuators = get_actuators_greenhouse(greenhouse_serial)

    users_roles = get_dic_users_role_greenhouse(greenhouse_serial)

    measures = {}

    if session.get('graph_start_date') and session.get('graph_end_date'):
        date_start = session['graph_start_date']
        date_end = session['graph_end_date']

    else:
        if not session.get('graph_delta_time'):
            session['graph_delta_time'] = 7
        date_start = datetime.utcnow() - timedelta(days=session['graph_delta_time'])
        date_end = datetime.utcnow()

    date_latest = datetime.utcnow() - timedelta(days=365)
    for data in get_data_sensors_since(greenhouse_serial, [sensor_id], date_start, date_end).values():
        for date, value in data.items():
            if date > date_latest:
                date_latest = date
            if sensor_type != "light":
                measures[date] = value / 10
            if sensor_type == "light":
                measures[date] = value

    targets = get_greenhouse_targets(greenhouse_serial)
    return render_template("pages/greenhouse_sensor.j2",
                           greenhouse_serial=greenhouse_serial,
                           sensor_id=sensor_id,
                           sensor_type=sensor_type,
                           sensor_unit=sensor_unit,
                           sidebar_sensors=sensors.items(),
                           sidebar_actuators=actuators.items(),
                           sidebar_users=users_roles.items(),
                           current_sidebar_item=('sensor', int(sensor_id)),
                           current_sensor_full_name=convert_sensor_type_to_full_name(sensor_type),
                           measures=measures,
                           ratio_measures=str(len(measures)) + ' sur ' + str(
                               get_number_of_measures(greenhouse_serial, sensor_id)),
                           date_latest=get_format_latest_measure(date_latest),
                           targets=targets,
                           from_datetime_utc=str(date_start),
                           to_datetime_utc=str(date_end),
                           from_date=date_start.strftime("%Y-%m-%d"),  # TODO: convert this to local time
                           to_date=date_end.strftime("%Y-%m-%d"))  # TODO: convert this to local time


def get_format_latest_measure(date_latest):
    diff = datetime.utcnow() - date_latest
    if diff < timedelta(minutes=1):
        return f"il y a {diff.seconds} secondes"
    elif diff < timedelta(hours=1):
        return f"il y a {diff.seconds // 60} minutes"
    elif diff < timedelta(days=1):
        return f"il y a {diff.seconds // 3600} heures"
    elif diff < timedelta(days=30):
        return f"il y a {diff.days} jours"
    else:
        return f"en {date_latest.strftime('%B')}"
