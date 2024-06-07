from flask import session, request, redirect, url_for

from src.database.greenhouse import get_role_user


def permission_manager():
	green_house_serial = request.form.get('ghs')
	user = request.form.get('user')
	role = request.form.get('role')

	if get_role_user(green_house_serial, session['user_name']) != 'owner':
		session['error'] = "Vous n'avez pas les permissions nécessaires pour effectuer cette action."

	else:
		# TODO : set the role `role` to the user `user`.
		pass

	return redirect(url_for('greenhouse_collaborator_page', greenhouse_serial=green_house_serial))
