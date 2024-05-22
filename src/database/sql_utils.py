from flask import g


def afficher_mesures_serre(greenhouse_id):
    cursor = g.db.connect().cursor()

    liste_mesures = []
    dic_mesures = {"temperature": [], "soil_humidity": [], "light": [], "air_humidity": [], "O2": [],
                   "water_level": []}
    try:
        cursor.execute(
            "SELECT Measures.sensor_id, Measures.date, Measures.value, Sensors.type, Sensors.unit FROM Measures, "
            "Sensors WHERE Measures.sensor_id = Sensors.id and Sensors.greenhouse_name= %s",
            name_serre)
        for (sensor_id, date, value, type, unit) in self.cursor:
            print(f"Mesure dans {name_serre} le {date}, faite par le capteur {sensor_id}, {type} de {value} {unit}")
            liste_mesures.append(
                f"Mesure dans {name_serre} le {date}, faite par le capteur {sensor_id}, {type} de {value} {unit}")
            dic_mesures[type].append([value, date, unit])
        return (liste_mesures, dic_mesures)

    except Exception as e:
        print(f"Erreur lors de l'affichage des mesures de la serre {name_serre}: {e}")

def afficher_actions_serre(greenhouse_id):
    """Affiche les actions de la serre name_serre"""

    try:
        cursor.execute(
            "SELECT Actions.actuator_id, Actions.date, Actions.value, Actuators.type FROM Actions, Actuators "
            "WHERE Actions.actuator_id = Actuators.id and Actuators.greenhouse_name= %s",
            name_serre)
        for (actuator_id, date, value, type) in self.cursor:
            print(f"Action dans {name_serre} le {date}, faite par l'actionneur {actuator_id}, {type} de {value}")

    except Exception as e:
        print(f"Erreur lors de l'affichage des actions de la serre {name_serre}: {e}")
