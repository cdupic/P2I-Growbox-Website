from flask import render_template, redirect, url_for

from src.utils.user import is_user_authenticated


def greenhouse_overview_page(greenhouse_id):
    if not is_user_authenticated():
        return redirect(url_for('login'))

    return render_template('pages/greenhouse_overview.j2', greenhouse_id=greenhouse_id)

