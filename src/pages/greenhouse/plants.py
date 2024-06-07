from flask import render_template, redirect, url_for, session

from src.database.greenhouse import (check_greenhouse_owner, get_greenhouse_name,
                                     get_greenhouse_targets, get_greenhouse_is_custom_config)
from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse
from src.database.plant import get_plants_greenhouse, get_data_plant, get_history_greenhouse
from src.utils.user import is_user_authenticated


def greenhouse_plants_page(greenhouse_serial):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))

    if not check_greenhouse_owner(session['user_name'], greenhouse_serial):
        session['error'] = f"La serre {greenhouse_serial} n'existe pas ou n'est pas accessible avec votre compte."
        return redirect(url_for('greenhouses_page'))

    current_plants = get_plants_greenhouse(greenhouse_serial)
    id_plants = [current_plants[plant][0] for plant in current_plants]
    nb_distinct_plants = len(set(id_plants))
    nb_crops = sum([current_plants[plant][1] for plant in current_plants])

    return render_template('pages/greenhouse_plants.j2',
                           current_sidebar_item=('plants', None),
                           greenhouse_serial=greenhouse_serial,
                           greenhouse_name=get_greenhouse_name(greenhouse_serial, session['user_name']),
                           sidebar_sensors=get_sensors_greenhouse(greenhouse_serial).items(),
                           sidebar_actuators=get_actuators_greenhouse(greenhouse_serial).items(),
                           is_custom_config=get_greenhouse_is_custom_config(greenhouse_serial),
                           # {id: (name, temperature, soil_humidity, air_humidity, light, O2)}
                           available_plants=get_data_plant(),
                           # {association_id: (plant_id, plant_name, count, start_date, end_date)}
                           old_plants=get_history_greenhouse(greenhouse_serial),
                           # {id: (plant_id, count, start_date, end_calculated_date)}
                           current_plants=current_plants,
                           # {temperature: 20, soil_humidity: 50, air_humidity: 60, light: 100}
                           targets=get_greenhouse_targets(greenhouse_serial),
                           nb_distinct_plants=nb_distinct_plants,
                           nb_crops=nb_crops)
