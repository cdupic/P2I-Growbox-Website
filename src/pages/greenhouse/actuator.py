from flask import redirect, url_for, session, render_template

from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse, get_data_actuators_since, \
    get_actuator_type
from src.utils.measure import convert_sensor_type_to_french
from src.utils.user import is_user_authenticated


def greenhouse_actuator_page(greenhouse_serial, actuator_id):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))

    # TODO: get the actuator type and data just like it is done in sensor.py.
    actuator_type = get_actuator_type(actuator_id)
    actuator_type_french = convert_sensor_type_to_french(actuator_type)

    sensors = get_sensors_greenhouse(greenhouse_serial)
    actuators = get_actuators_greenhouse(greenhouse_serial)

    measures_actuator = {}
    for measure in get_data_actuators_since(greenhouse_serial, [actuator_id], session['graphs_days']).values():
        for date, value in measure.items():
            measures_actuator[date] = value


    return render_template('pages/greenhouse_actuator.j2',
                           greenhouse_serial=greenhouse_serial,
                           sidebar_sensors=sensors.items(),
                           current_sidebar_item=('actuator', int(actuator_id)),
                           sidebar_actuators=actuators.items())
