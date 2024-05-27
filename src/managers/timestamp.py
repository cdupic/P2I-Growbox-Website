from flask import render_template, session, request
from datetime import datetime


from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse


def timestamp_manager():
	greenhouse_serial = session['serial']

	if 'start_date' in request.form and 'end_date' in request.form:

		start_date = datetime.strptime(request.form.get('start_date'), "%Y-%m-%d").date()
		end_date = datetime.strptime(request.form.get('end_date'), "%Y-%m-%d").date()
		session['graphs_days'] = (end_date - start_date).days
		print(session['graphs_days'])


	return render_template("pages/timestamp.j2",
									   greenhouse_serial=greenhouse_serial,
									   sidebar_sensors=get_sensors_greenhouse(greenhouse_serial).items(),
									   sidebar_actuators=get_actuators_greenhouse(greenhouse_serial).items(),
									   current_sidebar_item=('timestamp'))
