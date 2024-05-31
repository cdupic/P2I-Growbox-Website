from datetime import datetime

from flask import session, request, redirect
from datetime import time


def timestamp_manager():
    if 'start_date' in request.form and 'end_date' in request.form:
        if request.form.get('start_date') != '' and request.form.get('end_date') != '':
            start_date = datetime.strptime(request.form.get('start_date'), "%Y-%m-%d").date()
            end_date = datetime.strptime(request.form.get('end_date'), "%Y-%m-%d").date()

            start_datetime_local = datetime.combine(start_date, time(0, 0))
            end_datetime_local = datetime.combine(end_date, time(23, 59))

            session['graphs_days'] = (end_datetime_local - start_datetime_local).days

    return redirect(request.form.get('r'))
