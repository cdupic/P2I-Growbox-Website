from flask import session, redirect, url_for


def logout_manager():
    if 'auth_token' in session:
        session.pop('auth_token')
    if 'user_name' in session:
        session.pop('user_name')

    session['success'] = 'Vous avez été déconnecté'
    return redirect(url_for('landing_page'))
