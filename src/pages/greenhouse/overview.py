from flask import render_template, redirect, url_for

from src.utils.user import is_user_authenticated


def greenhouse_overview_page(greenhouse_serial):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))

    # TODO: Check that greenhouse_serial exists and belongs to the user (else redirect to the user greenhouses page).
    # TODO: Fetch the greenhouse name and the list of sensors and actuators (for displaying links).
    # TODO: Fetch data for each sensors in the last n days where n = session['graphs_days']
    # TODO: Pass all the data to the template.

    return render_template('pages/greenhouse_overview.j2', greenhouse_serial=greenhouse_serial)

