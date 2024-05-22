from flask import Flask, render_template, request, url_for, session, redirect
from dotenv import load_dotenv
import os
from random import randint
from lecture_SQL import SQL_lecture
import requests
import json
import time

load_dotenv() #quand chargé rend accessible les variables d'environnement du fichier .env das tout le script python
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
user_connected = False

@app.route('/')
def index():
	if 'nom_utilisateur' in session:
		return render_template('page_utilisateur.html')
	return render_template('index.html')

@app.route('/getserres')
def get_serres():
	return render_template('getserres.html')

@app.route('/test1')
def test1():
	return render_template('page_utilisateur.html')

# @app.route('/traitement', methods=['POST'])
# def traitement():
# 	if request.method == 'POST':
# 		serre = request.form.get('serre')
# 		sql = SQL_lecture()
# 		mesures = sql.afficher_mesures_serre(serre)
# 		print(mesures)
# 		if not mesures :
# 			#mesures = ["Aucune mesure pour cette serre"]
# 			return redirect('/getserres')
# 		else :
# 			return render_template('mesures.html', mesures=mesures)
#
# @app.route('/mesures')
# def mesures():
# 	sql = SQL_lecture()
# 	mesures = sql.afficher_mesures_serre("serre1")
#
# 	return render_template('mesures.html', mesures=mesures)

@app.route('/compteur')

def compteur():
	# si la clé "compteur" n'existe pas dans la session, on la crée
	if "compteur" not in session:
		session["compteur"] = 1
	else:
		session["compteur"] += 1
	return f"Nombre de visites : {session['compteur']}"

utilisateurs = [{"nom":"test","mdp":"test"}]


def recherche_utilisateur(nom, mdp):
	for utilisateur in utilisateurs:

		if utilisateur['nom']==nom and utilisateur['mdp']==mdp:
			print('valide')
			return utilisateur
	return None


@app.route("/lectureserre", methods=["POST", "GET"])
def lecture_serres():
	"""méthode permettant de voir les serres de l'utilisateur"""
	if user_connected:
		if session.get('nom_utilisateur') == "test":
			return render_template('lectureserres.html', serres=["serre1", "serre2", "serre3"])
		else:
			return render_template('lectureserres.html', serres=["aucune"])

	else :
		return redirect(url_for('login'))


dic_mesures = {}
liste_capteurs_mesures = []

@app.route("/infoserre/<serre_selectionnee>", methods=["POST", "GET"])

def info_serre(serre_selectionnee):
	"""méthode permettant de voir les infos de la serre sélectionnée"""
	global dic_mesures, liste_capteurs_mesures

	if user_connected:
		sql = SQL_lecture()
		mesures = sql.afficher_mesures_serre(serre_selectionnee)[0]
		dic_mesures = sql.afficher_mesures_serre(serre_selectionnee)[1]
		print(1, dic_mesures)
		for capteur, elements in dic_mesures.items():
			if len(elements)>0:
				liste_capteurs_mesures.append(capteur)
		if not mesures :

			mesures = ["Aucune mesure pour cette serre"]
			#return redirect('/serres')
			return render_template('mesures.html', mesures=mesures, serre_selectionnee=serre_selectionnee)
		else :
			return render_template('infoserre.html', liste_capteurs=liste_capteurs_mesures, dic_mesures=dic_mesures)

	else:
		return redirect(url_for('login'))


def tri_mesures(mesures):
	"""méthode permettant de trier les mesures par date"""
	mesures_triees = sorted(mesures, key=lambda x: x['date'], reverse=True)
	return mesures_triees

@app.route("/login", methods=["POST", "GET"])
def login():
	global user_connected
	print(session)
	if request.method == "POST":
		donnees = request.form
		nom = donnees.get('nom')
		mdp = donnees.get('mdp')
		utilisateur = recherche_utilisateur(nom, mdp)

		if utilisateur is not None:
			session['nom_utilisateur'] = utilisateur['nom']
			user_connected = True
			return render_template("page_utilisateur.html")
			#return redirect(url_for('index'))
		else:
			return redirect(url_for('login'))
	else: #importer car on peut accéder directement à la page depuis l'url donc risque de bypass
		if 'nom_utilisateur' in session:
			user_connected = True
			return render_template("page_utilisateur.html")
			#return redirect(url_for('index'))
		else:
			return render_template("login.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
	global user_connected
	session.pop('nom_utilisateur', None)
	user_connected = False
	return redirect(url_for('index'))



@app.route("/traitement", methods=["POST", "GET"])
def traitement():
	if request.method == "POST":
		donnees = request.form
		nom = donnees.get('nom')
		mdp = donnees.get('mdp')
		if nom == 'test' and mdp == 'test':
			return render_template("traitement.html", nom_utilisateur=nom)
		else:
			return render_template("traitement.html")
	else:
		return redirect('/index')



@app.route('/jeu', methods=["POST", "GET"])

def jeu():
	if request.method == "POST":
		reponse = int(request.form.get('nombre'))
		if reponse == session['nb']:
			message = "Bravo, vous avez trouvé le nombre mystère"
		elif reponse < session['nb']:
			message = "Le nombre mystère est plus grand"
		elif reponse > session['nb']:
			message = "Le nombre mystère est plus petit"
		return render_template("nombre-mystere.html", message=message)

	else:
		nb_mystere = randint(0, 100)
		session['nb'] = nb_mystere
		print(session)
		return render_template("nombre-mystere.html")


@app.route("/test" , methods=['POST'])
def test():
	if user_connected:
		if request.method == 'POST':
			select = request.form.get('capteur')
			print(str(select))
			valeurs = dic_mesures.get(select)
			print(dic_mesures, 'dic_mesures')
			print(valeurs)
			return render_template("infoserre.html", valeurs=valeurs, liste_capteurs=liste_capteurs_mesures, capteur_selectionne=select)
		return render_template("infoserre.html", valeurs=[], liste_capteurs=liste_capteurs_mesures)

	else:
		return redirect(url_for('login'))



if __name__ == '__main__':
	app.run(debug=True)

