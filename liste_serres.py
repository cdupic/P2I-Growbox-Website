from flask import render_template, session, redirect, url_for


def lecture_serres():
	"""méthode permettant de voir les serres de l'utilisateur"""
	if 'nom_utilisateur' in session:
		if session.get('nom_utilisateur') == "test":
			return render_template('lectureserres.html', serres=["serre1", "serre2", "serre3"])
		else:
			return render_template('lectureserres.html', serres=["aucune"])

	else :
		return redirect(url_for('login'))



