from flask import render_template

from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse
from src.database.greenhouse import get_dic_users_role_greenhouse

def greenhouse_collaborator_page(greenhouse_serial):

	sensors = get_sensors_greenhouse(greenhouse_serial)
	actuators = get_actuators_greenhouse(greenhouse_serial)
	collaborators_role = get_dic_users_role_greenhouse(greenhouse_serial)

	return render_template('pages/greenhouse_collaborators.j2',
						   greenhouse_serial=greenhouse_serial,
						   sidebar_sensors=sensors.items(),
						   sidebar_actuators=actuators.items(),
						   current_sidebar_item=('collaborator', None),
						   collaborators_role=collaborators_role)