from flask import render_template

from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse
from src.database.greenhouse import get_greenhouse_notification_date


def greenhouse_notification_page(greenhouse_serial):
	sensors = get_sensors_greenhouse(greenhouse_serial)
	actuators = get_actuators_greenhouse(greenhouse_serial)

	return render_template("pages/greenhouse_notification.j2",
						   greenhouse_serial=greenhouse_serial,
						   sidebar_sensors=sensors.items(),
						   sidebar_actuators=actuators.items(),
						   notifications=get_greenhouse_notification_date(greenhouse_serial),
						   current_sidebar_item=('notification', None))
