from flask import session, request, redirect, url_for

from src.database.greenhouse import get_role_user


def permission_manager():
	# TODO:
	#       If the parameter 'is-custom' is True,
	#           the config is specified as post parameters, e.g. 'temperature' = 25
	#           the code should update the greenhouse in the GreenHouses table and switch is_custom_config to true.

	if get_role_user(session['serial'], session['user_name']) != 'owner':
		session['error'] = "Vous n'avez pas les permissions nécessaires pour effectuer cette action."

	return redirect(url_for('greenhouse_collaborator_page', greenhouse_serial=request.form.get('ghs')))
