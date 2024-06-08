from flask import session, request, redirect, url_for

from src.database.greenhouse import get_user_role, set_user_role, create_new_role_notification


def permission_manager():
	greenhouse_serial = request.form.get('ghs')
	user = request.form.get('user')
	role = request.form.get('role')

	if get_user_role(greenhouse_serial, session['user_name']) != 'owner':
		session['error'] = "Vous n'avez pas les permissions nécessaires pour effectuer cette action."

	else:
		# TODO : set the role `role` to the user `user`.
		set_user_role(greenhouse_serial, user, role)
		create_new_role_notification(greenhouse_serial, user, role)

		pass

	return redirect(url_for('greenhouse_collaborator_page', greenhouse_serial=green_house_serial))
