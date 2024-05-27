def convert_sensor_type_to_french(sensor_type):
    if sensor_type == "temperature":
        return "Température"
    elif sensor_type == "soil_humidity":
        return "Humidité du sol"
    elif sensor_type == "light":
        return "Luminosité"
    elif sensor_type == "air_humidity":
        return "Humidité de l'air"
    elif sensor_type == "water_level":
        return "Niveau d'eau"
    elif sensor_type == "O2":
        return "O2"
    return "Inconnu"

def convert_actuator_type_to_french(sensor_type):
    if sensor_type == "temperature":
        return "refroidisseur"
    elif sensor_type == "soil_humidity":
        return "arrosage"
    elif sensor_type == "light":
        return "velux"
    elif sensor_type == "air_humidity":
        return "brumisateur"
    elif sensor_type == "water_level":
        return "robinet"
    elif sensor_type == "O2":
        return "ouveerture"
    return "Inconnu"