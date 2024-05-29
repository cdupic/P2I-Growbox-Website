from flask import render_template, redirect, url_for, session

from src.database.greenhouse import get_greenhouse_targets
from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse, get_data_sensors_since, \
    get_sensor_type, get_sensor_unit
from src.utils.measure import convert_sensor_type_to_french
from src.utils.user import is_user_authenticated
from datetime import datetime, timedelta


def greenhouse_sensor_page(greenhouse_serial, sensor_id):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))

    sensor_type = get_sensor_type(sensor_id)
    sensor_type_french = convert_sensor_type_to_french(sensor_type)
    sensor_unit = get_sensor_unit(sensor_id)

    sensors = get_sensors_greenhouse(greenhouse_serial)
    actuators = get_actuators_greenhouse(greenhouse_serial)

    measures = {}
    for data in get_data_sensors_since(greenhouse_serial, [sensor_id], session['graphs_days']).values():
        for date, value in data.items():
            if sensor_type != "light":
                measures[date] = value / 10
            else:
                measures[date] = value

    targets = get_greenhouse_targets(greenhouse_serial)
    return render_template("pages/greenhouse_sensor.j2",
                           greenhouse_serial=greenhouse_serial,
                           sensor_id=sensor_id,
                           sensor_type=sensor_type,
                           sensor_unit=sensor_unit,
                           sidebar_sensors=sensors.items(),
                           sidebar_actuators=actuators.items(),
                           current_sidebar_item=('sensor', int(sensor_id)),
                           measures=measures,
                           targets=targets,
                           from_date=str(datetime.utcnow() - timedelta(days=session['graphs_days'])),
                           to_date=str(datetime.utcnow()))
