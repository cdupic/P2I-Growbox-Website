from flask import render_template, redirect, url_for, session

from src.database.greenhouse import check_greenhouse_owner, get_dic_users_role_greenhouse, get_greenhouse_name
from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse
from src.utils.user import is_user_authenticated


def greenhouse_plants_page(greenhouse_serial):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))

    if not check_greenhouse_owner(session['user_name'], greenhouse_serial):
        session['error'] = f"La serre {greenhouse_serial} n'existe pas ou n'est pas accessible avec votre compte."
        return redirect(url_for('greenhouses_page'))

    # List of all plant ids available and their data
    # available_plants = {id: (name, temperature, soil_humidity, air_humidity, light, O2)}

    # List of current plants ids in the greenhouse with start date
    # current_plants = {id: (plant_id, count, start_date, None)}

    # List of plants ids that were in the greenhouse with start and end date
    # old_plants = {association_id: (plant_id, count, start_date, end_date)}

    return render_template('pages/greenhouse_plants.j2',
                           greenhouse_name=get_greenhouse_name(greenhouse_serial, session['user_name']),
                           sidebar_sensors=get_sensors_greenhouse(greenhouse_serial).items(),
                           sidebar_actuators=get_actuators_greenhouse(greenhouse_serial).items(),
                           sidebar_users=get_dic_users_role_greenhouse(greenhouse_serial).items(),
                           current_sidebar_item=('plants', None),
                           # plants_in_greenhouse=get_plants_greenhouse(greenhouse_serial),
                           # plants_history_greenhouse=get_history_greenhouse(greenhouse_serial),
                           available_plants={1: ('Tomate', 25, 50, 60, 100, 21), 2: ('Basilic', 25, 50, 60, 100, 21),
                                             3: ('Piment', 25, 50, 60, 100, 21), 4: ('Persil', 25, 50, 60, 100, 21)},
                           current_plants={1: (1, 2, '2021-01-01', None), 2: (2, 1, '2021-01-01', None)},
                           old_plants={3: (3, 2, '2021-01-01', '2021-01-15'), 4: (4, 1, '2021-01-01', '2021-01-15')},
                           greenhouse_serial=greenhouse_serial)
