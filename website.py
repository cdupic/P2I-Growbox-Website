from flask import Flask, render_template, request, redirect
from lecture_SQL import SQL_lecture
import requests
import json
import time

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/getserres')
def serres():
	return render_template('getserres.html')

@app.route('/traitement', methods=['POST'])
def traitement():
	if request.method == 'POST':
		serre = request.form.get('serre')
		sql = SQL_lecture()
		mesures = sql.afficher_mesures_serre(serre)
		print(mesures)
		if not mesures :
			#mesures = ["Aucune mesure pour cette serre"]
			return redirect('/getserres')
		else :
			return render_template('mesures.html', mesures=mesures)

@app.route('/mesures')
def mesures():
	sql = SQL_lecture()
	mesures = sql.afficher_mesures_serre("serre1")

	return render_template('mesures.html', mesures=mesures)



if __name__ == '__main__':
	app.run(debug=True)

