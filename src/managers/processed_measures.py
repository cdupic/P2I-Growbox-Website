from flask import session, request, redirect


def processed_measures_manager():
    session['processed_measures'] = request.form.get('processed_measures') == 'on'

    return redirect(request.form.get('r'))
