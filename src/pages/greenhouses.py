from flask import render_template, session, redirect, url_for

from src.database.greenhouse import get_greenhouses
from src.utils.user import is_user_authenticated


def greenhouses_page():
    if not is_user_authenticated():
        return redirect(url_for('login_page'))


    user_name = session['user_name']
    user_greenhouses = get_greenhouses(user_name)
    if 'processed_measures_choosed' not in session:
        session['processed_measures_choosed'] = True

    return render_template('pages/greenhouses.j2', user_greenhouses=user_greenhouses.items())






