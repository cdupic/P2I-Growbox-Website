from flask import session, redirect, url_for, request

from src.utils.user import create_user


def signup_manager():
    if 'user_name' in request.form and 'password' in request.form:
        auth_token = create_user(request.form['user_name'], request.form['password'])
        if auth_token is not None:
            session['user_name'] = request.form['user_name']
            session['auth_token'] = auth_token
            session['graphs_days'] = 7
            session['success'] = 'Votre compte a été créé avec succès'
            return redirect(url_for('greenhouses_page'))

        else:
            session['error'] = "Ce nom d'utilisateur est déjà utilisé"
            session['form_user_name'] = request.form['user_name']

    else:
        session['error'] = "Veuillez remplir les champs"

    return redirect(url_for('signup_page'))
