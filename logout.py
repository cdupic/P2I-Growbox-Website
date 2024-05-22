from flask import session, redirect, url_for


def logout():
	session.pop('nom_utilisateur', None)
	return redirect(url_for('index'))