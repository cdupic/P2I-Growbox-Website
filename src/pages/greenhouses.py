from flask import render_template, session, redirect, url_for

from src.utils.user import is_user_authenticated
from src.database.database import get_db


def greenhouses_page():
    if not is_user_authenticated():
        return redirect(url_for('login'))

    user_name = session['user_name']
    user_greenhouses = get_greenhouses(user_name)

    return render_template('pages/greenhouses.j2', user_greenhouses=user_greenhouses.items())


def get_greenhouses(user_name):
    db = get_db()
    cursor = db.cursor()
    greenhouses = {}

    try:
        cursor.execute(
            "SELECT name "
            "FROM GreenHouses "
            "WHERE user_name = %s",
            (user_name,)
        )
        for (greenhouse_name,) in cursor:
            greenhouses['name'] = greenhouse_name

        return greenhouses

    except Exception as e:
        print(f"Error when getting greenhouses: {e}")




