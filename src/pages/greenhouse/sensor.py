from flask import render_template, redirect, url_for, session

from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse, get_data_sensors_since, \
    get_sensor_type
from src.utils.measure import convert_sensor_type_to_french
from src.utils.user import is_user_authenticated


def greenhouse_sensor_page(greenhouse_serial, sensor_id):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))

    # TODO: get the sensor type for display + create a function that converts a sensor type to french
    sensor_type = get_sensor_type(sensor_id)
    sensor_type_french = convert_sensor_type_to_french(sensor_type)

    sensors = get_sensors_greenhouse(greenhouse_serial)
    actuators = get_actuators_greenhouse(greenhouse_serial)

    # TODO: get the measures for the last n days (session['graphs_days']):
    #   a dictionary with date as key and value as value.
    measures_sensor = {}
    for measure in get_data_sensors_since(greenhouse_serial, [sensor_id], session['graphs_days']).values():
        for date, value in measure.items():
            measures_sensor[date] = value

    return render_template("pages/greenhouse_sensor.j2",
                           sensors=sensors.items(),
                           actuators=actuators.items(),
                           measures=measures_sensor)

