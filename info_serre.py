from flask import render_template, session, redirect, url_for, request
from lecture_SQL import SQL_lecture


def info_serre(serre_selectionnee):
	"""méthode permettant de voir les infos de la serre (afficge uniquement les capteurs qui ont des mesures)"""
	sql = SQL_lecture()
	liste_capteurs_mesures = []
	if 'nom_utilisateur' in session:
		mesures = sql.afficher_mesures_serre(serre_selectionnee)[0]
		dic_mesures = sql.afficher_mesures_serre(serre_selectionnee)[1]
		for capteur, elements in dic_mesures.items():
			if len(elements) > 0:
				liste_capteurs_mesures.append(capteur)
		if not mesures:

			mesures = ["Aucune mesure pour cette serre"]
			#return redirect('/serres')
			return render_template('mesures.html', mesures=mesures, serre_selectionnee=serre_selectionnee)
		else :
			return render_template('infoserre.html', liste_capteurs=liste_capteurs_mesures, dic_mesures=dic_mesures, serre_selectionnee=serre_selectionnee)

	else:
		return redirect(url_for('login'))


