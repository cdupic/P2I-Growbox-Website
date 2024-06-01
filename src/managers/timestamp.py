from datetime import datetime, time, timedelta

import pytz
from flask import session, request, redirect


def timestamp_manager():
    if ('start_date' not in request.form or 'end_date' not in request.form
            or request.form.get('start_date') == '' or request.form.get('end_date') == ''):
        session['error'] = "La date sélectionnée est invalide."
        return redirect(request.form.get('r'))

    start_date = datetime.strptime(request.form.get('start_date'), "%Y-%m-%d").date()
    end_date = datetime.strptime(request.form.get('end_date'), "%Y-%m-%d").date()
    now = datetime.now()
    now_time = time(now.hour, now.minute, now.second)
    start_datetime_local = datetime.combine(start_date, now_time)
    end_datetime_local = datetime.combine(end_date, now_time)
    start_datetime_utc = start_datetime_local.astimezone(pytz.utc)
    end_datetime_utc = end_datetime_local.astimezone(pytz.utc)

    if end_datetime_utc < start_datetime_utc:
        session['error'] = "La date de fin doit être postérieure à la date de début."
        return redirect(request.form.get('r'))

    if start_datetime_local != end_datetime_local and abs(now-end_datetime_local) < timedelta(minutes=1):
        # Gliding window mode
        session['graph_delta_time'] = (end_datetime_utc - start_datetime_utc).days

        session['graph_start_date'] = None
        session['graph_end_date'] = None
        session['success'] = f"Vue actualisée sur {(end_datetime_utc - start_datetime_utc).days +1} jours."


    elif (datetime.combine(start_datetime_utc, time(0, 0, 0)) ==
          datetime.combine(end_datetime_utc, time(0, 0, 0))):

        # Real time mode
        session['graph_delta_time'] = 0
        session['graph_start_date'] = None
        session['graph_end_date'] = None
        session['success'] = f"Vue actualisée sur les mesures d'ajourd'hui."
    else:
        # Start and end date mode
        session['graph_start_date'] = datetime.combine(start_datetime_utc, time(0, 0, 0))
        session['graph_end_date'] = end_datetime_utc
        session['graphs_delta_time'] = None

        session['success'] = f"Vue actualisée sur {(end_datetime_utc - start_datetime_utc).days + 1} jours."
    return redirect(request.form.get('r'))



