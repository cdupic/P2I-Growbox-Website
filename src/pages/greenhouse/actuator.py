from flask import redirect, url_for

from src.utils.user import is_user_authenticated


def greenhouse_actuator_page(greenhouse_name, actuator_id):
    if not is_user_authenticated():
        return redirect(url_for('login'))

    return "Unimplemented"
