from flask import render_template


def landing_page():
    return render_template('pages/index.j2')
