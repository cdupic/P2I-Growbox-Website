from flask import redirect, url_for, session

from src.utils.user import is_user_authenticated
from src.database.database import get_actuator_type
from src.database.database import get_data_actuators_since


def greenhouse_actuator_page(greenhouse_name, actuator_id):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))

    # TODO: get the actuator type and data just like it is done in sensor.py.
    actuator_type = get_actuator_type(actuator_id)
    actuator_type_french = convert_actuator_type_to_french(actuator_type)

    measures_actuator = {}
    for measure in get_data_actuators_since(greenhouse_name, [actuator_id], session['graphs_days']).values():
        for date, value in measure.items():
            measures_actuator[date] = value

    return "Unimplemented"


def convert_actuator_type_to_french(actuator_type):
    if actuator_type == "temperature":
        return "température"
    elif actuator_type == "soil_humidity":
        return "humidité du sol"
    elif actuator_type == "luminosity":
        return "luminosité"
    elif actuator_type == "air_humidity":
        return "humidité de l'air"
    elif actuator_type == "water_level":
        return "niveau d'eau"