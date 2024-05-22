from flask import render_template, session, redirect, url_for

from src.utils.user import is_user_authenticated


def greenhouses_page():
    if not is_user_authenticated():
        return redirect(url_for('login'))

    user_name = session['user_name']
    # TODO: Get user greenhouses from database
    user_greenhouses = {
        "id1": "GreenHouse 1",
        "id2": "GreenHouse 2",
        "id3": "GreenHouse 3"
    }

    return render_template('pages/greenhouses.j2', user_greenhouses=user_greenhouses)
