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
        return "Chauffage/Climatisation"
    elif sensor_type == "soil_humidity":
        return "Arroseur"
    elif sensor_type == "light":
        return "Vélux"
    elif sensor_type == "air_humidity":
        return "Humidificateur"
    elif sensor_type == "water_level":
        return "Robinet"
    elif sensor_type == "O2":
        return "Ouverture"
    return "Inconnu"

def convert_sensor_type_to_full_name(sensor_type):
    if sensor_type == "temperature":
        return "Capteur de température (°C)"
    elif sensor_type == "soil_humidity":
        return "Capteur d'humidité du sol (%HR)"
    elif sensor_type == "light":
        return "Capteur de luminosité (lux)"
    elif sensor_type == "air_humidity":
        return "Capteur d'humidité de l'air (%HR)"
    elif sensor_type == "water_level":
        return "Capteur de niveau d'eau (mm)"
    elif sensor_type == "O2":
        return "Capteur d'O2 (%)"
    return "Capteur Inconnu"

def convert_actuator_type_to_full_name(sensor_type):
    if sensor_type == "temperature":
        return "Pompe à chaleur"
    elif sensor_type == "soil_humidity":
        return "Pompe à eau"
    elif sensor_type == "light":
        return "Vélux"
    elif sensor_type == "air_humidity":
        return "Humidificateur"
    elif sensor_type == "water_level":
        return "Robinet"
    elif sensor_type == "O2":
        return "Ouverture"
    return "Inconnu"
