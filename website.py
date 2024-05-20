from flask import Flask, render_template, request, url_for, session, redirect
#from lecture_SQL import SQL_lecture
import requests
import json
import time

app = Flask(__name__)
app.secret_key ="57d029fa9a23e8757753103d9130227dbba262963769cbd1b858d41990b4bbe1"

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/getserres')
def serres():
	return render_template('getserres.html')

@app.route('/test')
def test():
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

utilisateurs = [
	{"nom" : "test",
	 "mdp" : "test"}
]

def recherche_utilisateur(nom, mdp):
	for utilisateur in utilisateurs:
		if utilisateur['nom']==nom and utilisateur['mdp']==mdp:
			print('valide')
			return utilisateur
	return None


@app.route("/login", methods=["POST", "GET"])
def login():
	print(session)
	if request.method == "POST":
		donnees = request.form
		nom = donnees.get('nom')
		mdp = donnees.get('mdp')
		utilisateur = recherche_utilisateur(nom, mdp)

		if utilisateur is not None:
			session['nom_utilisateur'] = utilisateur['nom']
			return redirect(url_for('index'))
		else:
			return redirect(url_for('login'))
	else: #importer car on peut accéder directement à la page depuis l'url donc risque de bypass
		if 'nom_utilisateur' in session:
			return redirect(url_for('index'))
		else:
			return render_template("login.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
	session.pop('nom_utilisateur', None)
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
if __name__ == '__main__':
	app.run(debug=True)

