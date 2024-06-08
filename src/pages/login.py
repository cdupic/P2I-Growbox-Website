from flask import render_template, redirect, url_for

from src.utils.user import is_user_authenticated


def login_page():
    if is_user_authenticated():
        return redirect(url_for('greenhouses_page'))

    return render_template("pages/login.j2")
