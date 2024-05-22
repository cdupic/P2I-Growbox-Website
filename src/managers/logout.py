from flask import session, redirect, url_for


def logout_manager():
    session.pop('user_name', None)
    session.pop('auth_token', None)
    return redirect(url_for('index'))
