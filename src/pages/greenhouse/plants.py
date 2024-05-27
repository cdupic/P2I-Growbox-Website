from flask import render_template, redirect, url_for, session

from src.database.greenhouse import check_greenhouse_owner
from src.utils.user import is_user_authenticated


def greenhouse_plants_page(greenhouse_serial):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))

    if not check_greenhouse_owner(session['user_name'], greenhouse_serial):
        session['error'] = f"La serre {greenhouse_serial} n'existe pas ou n'est pas accessible avec votre compte."
        return redirect(url_for('greenhouses_page'))

    # TODO: Get the list of ALL the plants ids and dates of this greenhouse (including ones that have an end date)
    #   Format {plant_id: (date_start, date_end)}}
    # TODO: Get the list of all the plants in the table Plants
    #   Format {plant_id: {'name': ..., 'temperature': ..., ...}})}

    return render_template('pages/greenhouse_plants.j2',
                           sidebar_sensors={'test': 'TG'}.items(),
                           sidebar_actuators={'test': 'Salut mec!'}.items(),
                           current_sidebar_item=('plants', None),
                           greenhouse_serial=greenhouse_serial)
