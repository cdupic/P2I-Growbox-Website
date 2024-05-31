from datetime import datetime, timedelta

from flask import render_template, redirect, url_for, session

from src.database.greenhouse import get_greenhouse_targets, get_dic_users_role_greenhouse
from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse, get_data_sensors_since, \
    get_sensor_type, get_sensor_unit
from src.utils.measure import convert_sensor_type_to_french, convert_sensor_type_to_full_name
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
    for data in get_data_sensors_since(greenhouse_serial, [sensor_id], session['graphs_days']).values():
        for date, value in data.items():
            if sensor_type != "light":
                measures[date] = value / 10
            else:
                measures[date] = value

    from_datetime_utc = datetime.utcnow() - timedelta(days=session['graphs_days'])
    to_datetime_utc = datetime.utcnow()

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
                           targets=targets,
                           from_datetime_utc=str(datetime.utcnow() - timedelta(days=session['graphs_days'])),
                           to_datetime_utc=str(datetime.utcnow()),
                           from_date=(datetime.now() - timedelta(days=session['graphs_days'])).strftime("%Y-%m-%d"),
                           to_date=datetime.now().strftime("%Y-%m-%d"))
