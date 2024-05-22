from flask import render_template, redirect, url_for, request

from src.utils.user import is_user_authenticated, authenticate_user


def login_page():
    if is_user_authenticated():
        # User already authenticated
        return redirect(url_for('greenhouse'))

    cant_find_user = False

    if request.method == "POST":
        if authenticate_user(request.form['user_name'], request.form['password']):
            return redirect(url_for('greenhouse'))
        else:
            cant_find_user = True

    return render_template("pages/login.j2", cant_find_user=cant_find_user)
