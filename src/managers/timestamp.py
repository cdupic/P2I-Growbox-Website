from datetime import datetime

from flask import session, request, redirect
from datetime import time


def timestamp_manager():
    if 'start_date' in request.form and 'end_date' in request.form:
        if request.form.get('start_date') != '' and request.form.get('end_date') != '':
            start_date = datetime.strptime(request.form.get('start_date'), "%Y-%m-%d").date()
            end_date = datetime.strptime(request.form.get('end_date'), "%Y-%m-%d").date()

            now = datetime.now()
            now_time = time(now.hour, now.minute, now.second)
            start_datetime_local = datetime.combine(start_date, now_time)
            end_datetime_local = datetime.combine(end_date, now_time)


            if now - end_datetime_local > timedelta(seconds=1):
                # Start and end date mode
                session['graph_start_date'] = start_datetime_local.date()
                session['graph_end_date'] = end_datetime_local.date()
            else:
                # Gliding window mode
                session['graphs_delta_time'] = end_datetime_local - start_datetime_local

    return redirect(request.form.get('r'))
