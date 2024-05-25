from flask import render_template, redirect, url_for, session

from src.database.sql_utils import get_greenhouse_measures
from src.database.database import get_sensor_type
from src.database.database import get_data_sensors_since

from src.utils.user import is_user_authenticated



def greenhouse_sensor_page(greenhouse_serial, sensor_id):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))

    # TODO: get the sensor type for display + create a function that converts a sensor type to french
    sensor_type = get_sensor_type(sensor_id)
    sensor_type_french = convert_sensor_type_to_french(sensor_type)

    # TODO: get the measures for the last n days (session['graphs_days']):
    #   a dictionary with date as key and value as value.
    measures_sensor = {}
    for measure in get_data_sensors_since(greenhouse_serial, [sensor_id], session['graphs_days']).values():
        for date, value in measure.items():
            measures_sensor[date] = value

    return render_template("pages/greenhouse_sensor.j2", measures=measures_sensor)


def convert_sensor_type_to_french(sensor_type):
    if sensor_type == "temperature":
        return "température"
    elif sensor_type == "soil_humidity":
        return "humidité du sol"
    elif sensor_type == "luminosity":
        return "luminosité"
    elif sensor_type == "air_humidity":
        return "humidité de l'air"
    elif sensor_type == "water_level":
        return "niveau d'eau"



