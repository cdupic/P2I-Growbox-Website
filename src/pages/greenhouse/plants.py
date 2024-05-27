from flask import render_template, redirect, url_for, session

from src.database.greenhouse import check_greenhouse_owner
from src.utils.user import is_user_authenticated


def greenhouse_plants_page(greenhouse_serial):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))

    if not check_greenhouse_owner(session['user_name'], greenhouse_serial):
        session['error'] = f"La serre {greenhouse_serial} n'existe pas ou n'est pas accessible avec votre compte."
        return redirect(url_for('greenhouses_page'))

    return render_template('pages/greenhouse_plants.j2',
                           sidebar_sensors={'test': 'TG'}.items(),
                           sidebar_actuators={'test': 'Salut mec!'}.items(),
                           current_sidebar_item=('plants', None),
                           greenhouse_serial=greenhouse_serial)
