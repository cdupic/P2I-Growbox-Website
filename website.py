from flask import Flask, render_template, request, url_for, session, redirect
from dotenv import load_dotenv
import os
from lecture_SQL import SQL_lecture

import requests

# import des fonctions des autres fichiers
import liste_serres
import login
import logout
import info_serre
import sensor_values

load_dotenv() #quand chargé rend accessible les variables d'environnement du fichier .env das tout le script python
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route('/')
def index():
	"""Page de base affichée quand on ouvre le site"""

	if 'nom_utilisateur' in session:
		return render_template('page_utilisateur.html')
	return render_template('index.html')


@app.route('/compteur')

def compteur():
	"""si la clé "compteur" n'existe pas dans la session, on la crée, fonction servant a afficher le nb de fois qu'on a consulté le site"""
	if "compteur" not in session:
		session["compteur"] = 1
	else:
		session["compteur"] += 1
	return f"Nombre de visites : {session['compteur']}"


app.add_url_rule("/lectureserre", methods=["POST", "GET"], view_func=liste_serres.lecture_serres)
app.add_url_rule("/login", methods=["POST", "GET"], view_func=login.login)
app.add_url_rule("/logout", methods=["POST", "GET"], view_func=logout.logout)
app.add_url_rule("/infoserre/<serre_selectionnee>", methods=["POST", "GET"], view_func=info_serre.info_serre)
app.add_url_rule("/serres/<serre_selectionnee>", methods=["POST", "GET"], view_func=sensor_values.sensor_values)

if __name__ == '__main__':
	app.run(debug=True, use_reloader=True)


