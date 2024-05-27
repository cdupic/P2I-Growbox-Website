def convert_sensor_type_to_french(sensor_type):
    if sensor_type == "temperature":
        return "Température"
    elif sensor_type == "soil_humidity":
        return "Humidité du sol"
    elif sensor_type == "luminosity":
        return "Luminosité"
    elif sensor_type == "air_humidity":
        return "Humidité de l'air"
    elif sensor_type == "water_level":
        return "Niveau d'eau"
    return "Inconnu"