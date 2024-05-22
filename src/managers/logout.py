from flask import session, redirect, url_for


def logout_manager():
    session.pop('user_id', None)
    return redirect(url_for('index'))
