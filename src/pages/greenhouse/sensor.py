from flask import render_template, redirect, url_for, session

from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse, get_data_sensors_since, \
    get_sensor_type, get_sensor_unit

from src.database.greenhouse import get_greenhouse_targets
from src.utils.measure import convert_sensor_type_to_french
from src.utils.user import is_user_authenticated


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
            measures[date] = value

    if sensor_type != "water_level":
        target_measure = get_greenhouse_targets(greenhouse_serial)[sensor_type]
        target_measure_list = []
        for i in range(len(measures.values())):
            target_measure_list.append(target_measure)

    else:
        # TODO : create a condition in js to not display second chart if sensor is water_level
        target_measure_list = [0 for _ in measures.values()]

    return render_template("pages/greenhouse_sensor.j2",
                           greenhouse_serial=greenhouse_serial,
                           sensor_type=sensor_type_french,
                           sensor_unit=sensor_unit,
                           sidebar_sensors=sensors.items(),
                           sidebar_actuators=actuators.items(),
                           current_sidebar_item=('sensor', int(sensor_id)),
                           measures=measures,
                           target_measure=target_measure_list)

