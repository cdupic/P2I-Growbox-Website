from flask import session, redirect, url_for, request

from src.database.greenhouse import link_greenhouse_to_user, verify_greenhouse_exists


def associate_manager():
    if verify_greenhouse_exists(request.args['ghs']):
        link_greenhouse_to_user(request.args['ghs'], session['user_name'])
        return redirect(url_for('greenhouses_page'))
