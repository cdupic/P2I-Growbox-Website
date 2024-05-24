from flask import g


def get_greenhouse_measures(greenhouse_id, sensor_id, date_begin, date_end):
    cursor = g.db.cursor
    measures = []

    try:
        cursor.execute(
            "SELECT Measures.sensor_id, Measures.date, Measures.value, Sensors.type, Sensors.unit "
            "FROM Measures, Sensors "
            "WHERE Measures.sensor_id = Sensors.id  and Sensors.id = %s and Sensors.greenhouse_serial= %s and "
            "Measures.date BETWEEN %s and %s ",
            (sensor_id, greenhouse_id, date_begin, date_end))

        for sensor in cursor:
            measures.append(sensor)

    except Exception as e:
        print(f"Erreur lors de l'affichage des mesures de la serre {greenhouse_id}: {e}")

    return measures


# TODO
def get_greenhouse_actions(greenhouse_id, actuator_id, date_debut, date_fin):
    cursor = g.db.connect().cursor()

    try:
        cursor.execute(
            "SELECT Actions.actuator_id, Actions.date, Actions.value, Actuators.type "
            "FROM Actions, Actuators "
            "WHERE Actions.actuator_id = Actuators.id and Actuators.id= %s and Actuators.greenhouse_serial= %s and "
            "Actions.date BETWEEN %s and %s",
            (actuator_id, greenhouse_id, date_debut, date_fin))

        for (actuator_id, date, value, sensor_type) in cursor:
            print(f"Action in {greenhouse_id} the {date}, done by actuator {actuator_id}, {sensor_type} : {value}")

    except Exception as e:
        print(f"Error when getting actions of greenhouse : {greenhouse_id}: {e}")
