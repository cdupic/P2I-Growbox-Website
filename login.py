from flask import render_template, session, redirect, url_for, request

utilisateurs = [{"nom":"test","mdp":"test"}]


def recherche_utilisateur(nom, mdp):
	"""méthode permettant de vérifier si l'utilisateur existe et si le mot de passe est correct"""
	for utilisateur in utilisateurs:

		if utilisateur['nom']==nom and utilisateur['mdp']==mdp:
			print('valide')
			return utilisateur
	return None

def login():
	if request.method == "POST":
		donnees = request.form
		nom = donnees.get('nom')
		mdp = donnees.get('mdp')
		utilisateur = recherche_utilisateur(nom, mdp)

		if utilisateur is not None:
			session['nom_utilisateur'] = utilisateur['nom']
			return render_template("page_utilisateur.html")
		#return redirect(url_for('index'))
		else:
			return redirect(url_for('login'))
	else: #importer car on peut accéder directement à la page depuis l'url donc risque de bypass
		if 'nom_utilisateur' in session:
			return render_template("page_utilisateur.html")
		#return redirect(url_for('index'))
		else:
			return render_template("login.html")