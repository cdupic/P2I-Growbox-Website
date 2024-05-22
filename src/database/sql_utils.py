from flask import g


def get_greenhouse_measures(greenhouse_id):
    cursor = g.db.connect().cursor()

    # TODO: parametrize the function to take in parameter the sensor_id and a date range
    measures = {"temperature": [], "soil_humidity": [], "light": [], "air_humidity": [], "O2": [],
                   "water_level": []}
    try:
        cursor.execute(
            "SELECT Measures.sensor_id, Measures.date, Measures.value, Sensors.type, Sensors.unit FROM Measures, "
            "Sensors WHERE Measures.sensor_id = Sensors.id and Sensors.greenhouse_name= %s",
            greenhouse_id)
        for (sensor_id, date, value, type, unit) in cursor:
            measures[type].append([value, date, unit])

        return measures

    except Exception as e:
        print(f"Erreur lors de l'affichage des mesures de la serre {greenhouse_id}: {e}")

def print_greenhouse_actions(greenhouse_id):
    cursor = g.db.connect().cursor()

    # TODO: parametrize the function to take in parameter the actuator_id and a date range
    try:
        cursor.execute(
            "SELECT Actions.actuator_id, Actions.date, Actions.value, Actuators.type FROM Actions, Actuators "
            "WHERE Actions.actuator_id = Actuators.id and Actuators.greenhouse_name= %s",
            greenhouse_id)

        for (actuator_id, date, value, type) in cursor:
            print(f"Action dans {greenhouse_id} le {date}, faite par l'actionneur {actuator_id}, {type} de {value}")

    except Exception as e:
        print(f"Erreur lors de l'affichage des actions de la serre {greenhouse_id}: {e}")
