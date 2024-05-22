from flask import render_template, session, redirect, url_for, request
from lecture_SQL import SQL_lecture

def sensor_values(serre_selectionnee):
	"""méthode permettant de voir les valeurs des capteurs de la serre sélectionnée en renvoyant à infoserre.html pour qu'il affiche la liste des mesures"""
	print('appelé')
	print('serre selecrtionnée :',serre_selectionnee)
	if 'nom_utilisateur' in session:
		if request.method == 'POST':
			sql = SQL_lecture()
			liste_capteurs_mesures = []

			select = request.form.get('capteur')
			print('select :',select)
			dic_mesures = sql.afficher_mesures_serre(serre_selectionnee)[1]

			valeurs = dic_mesures.get(select)
			print('valeurs :',valeurs)
			for capteur, elements in dic_mesures.items():
				if len(elements) > 0:
					liste_capteurs_mesures.append(capteur)


			return render_template("infoserre.html", valeurs=valeurs, liste_capteurs=liste_capteurs_mesures, capteur_selectionne=select, serre_selectionnee=serre_selectionnee)
		return render_template("infoserre.html", valeurs=[], liste_capteurs=liste_capteurs_mesures)

	else:
		return redirect(url_for('login'))