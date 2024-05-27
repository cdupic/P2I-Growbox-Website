from flask import render_template, session
from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse


def timestamp_manager():
	greenhouse_serial = session['serial']
	return render_template("pages/greenhouse_sensor.j2",
						   greenhouse_serial=greenhouse_serial,
						   sidebar_sensors=get_sensors_greenhouse(greenhouse_serial).items(),
						   sidebar_actuators=get_actuators_greenhouse(greenhouse_serial).items(),
						   current_sidebar_item=('timestamp'))