from datetime import datetime, timedelta

from flask import render_template, redirect, url_for

from src.database.greenhouse import get_greenhouse_targets
from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse, get_data_sensors_since, \
    get_sensor_type, get_sensor_unit, get_number_of_measures, get_date_end_start, get_format_latest_measure
from src.database.analysis_O2 import order_data
from src.utils.sensor_names import convert_sensor_type_to_french, convert_sensor_type_to_full_name
from src.utils.user import is_user_authenticated


def greenhouse_sensor_page(greenhouse_serial, sensor_id):
    if not is_user_authenticated():
        return redirect(url_for('login_page'))

    sensor_type = get_sensor_type(sensor_id)
    sensor_type_french = convert_sensor_type_to_french(sensor_type)
    sensor_unit = get_sensor_unit(sensor_id)

    sensors = get_sensors_greenhouse(greenhouse_serial)
    actuators = get_actuators_greenhouse(greenhouse_serial)

    measures = {}
    total_measures_sensor = get_number_of_measures(greenhouse_serial, sensor_id)
    date_start, date_end = get_date_end_start()
    date_latest = datetime.utcnow() - timedelta(days=365)

    for data in get_data_sensors_since(greenhouse_serial, [sensor_id], date_start, date_end).values():
        for date, value in data.items():
            if date > date_latest:
                date_latest = date
            measures[date] = value

    targets = get_greenhouse_targets(greenhouse_serial)

    if measures != {} or total_measures_sensor:
        date_latest = get_format_latest_measure(date_latest)
    else:
        date_latest = None

    data_analysed_O2_night, data_analysed_O2_day = order_data(sensor_id)

    return render_template("pages/greenhouse_sensor.j2",
                           greenhouse_serial=greenhouse_serial,
                           sensor_id=sensor_id,
                           sensor_type=sensor_type,
                           sensor_type_french=sensor_type_french,
                           sensor_unit=sensor_unit,
                           sidebar_sensors=sensors.items(),
                           sidebar_actuators=actuators.items(),
                           current_sidebar_item=('sensor', int(sensor_id)),
                           current_sensor_full_name=convert_sensor_type_to_full_name(sensor_type),
                           measures=measures,
                           data_analysed_O2_night=data_analysed_O2_night,
                           data_analysed_O2_day=data_analysed_O2_day,
                           date_selected_measures=len(measures),
                           total_measures_sensor=total_measures_sensor,
                           date_latest=date_latest,
                           targets=targets,
                           from_datetime_utc=str(date_start),
                           to_datetime_utc=str(date_end))
