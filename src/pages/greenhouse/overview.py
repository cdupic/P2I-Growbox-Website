from flask import render_template, redirect, url_for, session

from src.database.greenhouse import check_greenhouse_owner, get_greenhouse_name, \
    get_greenhouse_targets, create_measures_notification
from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse, get_data_all_sensors, \
    get_number_measures, get_date_end_start, get_date_latest_measure, get_format_latest_measure
from src.utils.user import is_user_authenticated


def greenhouse_overview_page(greenhouse_serial):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))
    if not check_greenhouse_owner(session['user_name'], greenhouse_serial):
        session['error'] = f"La serre {greenhouse_serial} n'existe pas ou n'est pas accessible avec votre compte."
        return redirect(url_for('greenhouses_page'))

    create_measures_notification(greenhouse_serial)
    print(session['processed_measures_choosed'])
    sensors = get_sensors_greenhouse(greenhouse_serial)
    actuators = get_actuators_greenhouse(greenhouse_serial)
    date_start, date_end = get_date_end_start()
    data_measures = get_data_all_sensors(greenhouse_serial, date_start, date_end, session['processed_measures_choosed'])
    total_measures = get_number_measures(greenhouse_serial, [], [], session['processed_measures_choosed'])
    targets = get_greenhouse_targets(greenhouse_serial)

    if data_measures != {} or total_measures:
        date_latest = get_date_latest_measure(greenhouse_serial, session['processed_measures_choosed'])
        date_latest = get_format_latest_measure(date_latest)

    else:
        date_latest = None

    print(total_measures, (get_number_measures(greenhouse_serial, date_start, date_end,
                                               session['processed_measures_choosed'])) )

    return render_template('pages/greenhouse_overview.j2',
                           greenhouse_serial=greenhouse_serial,
                           sidebar_sensors=sensors.items(),
                           sidebar_actuators=actuators.items(),
                           date_selected_measures=get_number_measures(greenhouse_serial, date_start, date_end,
                                                                      session['processed_measures_choosed']),
                           total_measures=total_measures,
                           current_sidebar_item=('overview', None),
                           data_sensors=data_measures,
                           targets=targets,
                           date_latest=date_latest,
                           greenhouse_name=get_greenhouse_name(greenhouse_serial, session['user_name']),
                           from_datetime_utc=str(date_start),
                           to_datetime_utc=str(date_end))
