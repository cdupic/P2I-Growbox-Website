from flask import session, redirect, url_for, request

from src.utils.user import authenticate_user


def login_manager():
    if 'user_name' in request.form and 'password' in request.form:
        if authenticate_user(request.form['user_name'], request.form['password']):
            session['success'] = 'Bon retour parmi nous !'
            return redirect(url_for('greenhouses_page'))

        session['error'] = "Nom d'utilisateur ou mot de passe invalide"
        session['form_user_name'] = request.form['user_name']

    else:
        session['error'] = "Veuillez remplir les champs"

    return redirect(url_for('login_page'))
