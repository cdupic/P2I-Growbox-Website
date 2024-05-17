import mysql.connector as mysql

class SQL_connection:

	"""Autre moyen de se connecter de façon automatique à la base de données"""

	def __init__(self):
		self.connexion = None
		self.cursor = None
		self.ouvrir_connexion_bd()

	def ouvrir_connexion_bd(self):
		"""Ouvre une connexion à la base de données"""

		print("")
		print("***********************")
		print("** Connexion à la BD **")
		print("***********************")

		try:
			self.connexion = mysql.connect(
				host="fimi-bd-srv1.insa-lyon.fr",
				port=3306,
				user="G221_A",      # à compléter
				password="G221_A",  # à compléter
				database="G221_A_BD3"   # à compléter
			)
			self.cursor = self.connexion.cursor()

		except Exception as e:
			if type(e) == NameError and str(e).startswith("name 'mysql'"):
				print("[ERROR] MySQL: Driver 'mysql' not installed ? (Python Exception: " + str(e) + ")")
				print("[ERROR] MySQL:" +
					  " Package MySQL Connector should be installed [Terminal >> pip install mysql-connector-python ]" +
					  " and imported in the script [import mysql.connector as mysql]")
			else:
				print("[ERROR] MySQL: " + str(e))

		if self.connexion is not None:
			print("=> Connexion établie...")
		else:
			print("=> Connexion échouée...")

		return self.connexion

	def fermer_connexion_bd(self):
		"""Ferme la connexion à la base de données"""

		if self.connexion is not None:
			self.connexion.close()
			print("=> Connexion fermée...")
		else:
			print("=> Connexion inexistante...")