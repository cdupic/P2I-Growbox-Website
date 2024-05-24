from flask import render_template, redirect, url_for, session

from src.utils.user import is_user_authenticated
from src.database.database import check_greenhouse_owner
from src.database.database import get_sensors_greenhouse
from src.database.database import get_actuators_greenhouse
from src.database.database import get_data_sensors_since



def greenhouse_overview_page(greenhouse_serial):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))

    # TODO: Check that greenhouse_serial exists and belongs to the user (else redirect to the user greenhouses page).
    user = session['user_name']
    if not check_greenhouse_owner(user, greenhouse_serial):
        return redirect(url_for('greenhouses_page'))

    # TODO: Fetch the greenhouse name and the list of sensors and actuators (for displaying links).
    sensors_list = get_sensors_greenhouse(greenhouse_serial)
    actuators_list = get_actuators_greenhouse(greenhouse_serial)

    # TODO: Fetch data for each sensors in the last n days where n = session['graphs_days']
    data_sensors = get_data_sensors_since(greenhouse_serial, sensors_list, session['graphs_days'])
    # TODO: Pass all the data to the template.

    return render_template('pages/greenhouse_overview.j2', greenhouse_serial=greenhouse_serial)



