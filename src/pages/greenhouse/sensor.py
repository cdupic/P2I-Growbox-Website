from flask import render_template, redirect, url_for

from src.database.sql_utils import get_greenhouse_measures
from src.utils.user import is_user_authenticated


def greenhouse_sensor_page(greenhouse_serial, sensor_id):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))

    measures = get_greenhouse_measures(greenhouse_serial)[1]
    return render_template("pages/greenhouse_sensor.j2", measures=measures)
