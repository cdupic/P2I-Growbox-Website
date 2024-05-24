#from flask import g
from sql_connexion_test import SQL_connection
from datetime import datetime


def get_greenhouse_measures(greenhouse_id, sensor_id, date_debut, date_fin):
    # cursor = g.db.connect().cursor()

    # j'utilise ici sql_connection pour me connecter à la base de données parce que g marche pas tant que le site est pas actif
    sql_connection = SQL_connection()
    cursor = sql_connection.cursor

    measures = {"temperature": [], "soil_humidity": [], "light": [], "air_humidity": [], "O2": [],
                   "water_level": []}
    try:

        cursor.execute(
            "SELECT Measures.sensor_id, Measures.date, Measures.value, Sensors.type, Sensors.unit "
            "FROM Measures, Sensors"
            " WHERE Measures.sensor_id = Sensors.id  and Sensors.id = %s and Sensors.serial_number= %s and Measures.date BETWEEN %s and %s ",
            (sensor_id, greenhouse_id, date_debut, date_fin))
        
        for (sensor_id, date, value, type, unit) in cursor:
            print(f"Mesure dans {greenhouse_id} le {date}, faite par le capteur {sensor_id}, {type} de {value} {unit}")
            measures[type].append([value, date, unit])

        sql_connection.fermer_connexion_bd()

        return measures

    except Exception as e:
        print(f"Erreur lors de l'affichage des mesures de la serre {greenhouse_id}: {e}")

def print_greenhouse_actions(greenhouse_id, actuator_id, date_debut, date_fin):
    #cursor = g.db.connect().cursor()

    # j'utilise ici sql_connection pour me connecter à la base de données parce que g marche pas tant que le site est pas actif
    sql_connection = SQL_connection()
    cursor = sql_connection.cursor

    try:
        cursor.execute(
            "SELECT Actions.actuator_id, Actions.date, Actions.value, Actuators.type FROM Actions, Actuators "
            "WHERE Actions.actuator_id = Actuators.id and Actuators.id= %s and Actuators.serial_number= %s and Actions.date BETWEEN %s and %s",
            (actuator_id, greenhouse_id, date_debut, date_fin))

        for (actuator_id, date, value, type) in cursor:
            print(f"Action dans {greenhouse_id} le {date}, faite par l'actionneur {actuator_id}, {type} de {value}")

        sql_connection.fermer_connexion_bd()

    except Exception as e:
        print(f"Erreur lors de l'affichage des actions de la serre {greenhouse_id}: {e}")


if __name__ == "__main__":
    # Example of use
    greenhouse_id = "test_serial"
    sensor_id = "1"
    actuator_id = "1"
    date_debut = datetime(2024, 1, 1)
    date_fin = datetime(2025, 1, 1)
    measures = get_greenhouse_measures(greenhouse_id, sensor_id, date_debut, date_fin)
    print(measures)
    print_greenhouse_actions(greenhouse_id, actuator_id, date_debut, date_fin)