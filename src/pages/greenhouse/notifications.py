from flask import render_template

from src.database.greenhouse import get_greenhouse_notifications
from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse


def greenhouse_notification_page(greenhouse_serial):
    sensors = get_sensors_greenhouse(greenhouse_serial)
    actuators = get_actuators_greenhouse(greenhouse_serial)

    notifications_translations = {
        'temperature': 'Température',
        'air_humidity': 'Humidité de l\'air',
        'soil_humidity': 'Humidité du sol',
        'light': 'Lumière',
        '02': 'Oxygène',
        'water_level': 'Niveau d\'eau',
        'new_member': 'Nouveau membre',
        'new_role': 'Rôles',
        'drop_plant': 'Suppression plantes',
        'new_plant': 'Nouvelle plante',
        'custom_config': 'Configuration manuelle',
        'greenhouse_connected': 'Serre connectée'
    }

    notifications_kinds = {
        'temperature': 'target',
        'air_humidity': 'target',
        'soil_humidity': 'target',
        'light': 'target',
        '02': 'target',
        'water_level': 'target',
        'new_member': 'info',
        'new_role': 'info',
        'drop_plant': 'info',
        'new_plant': 'info',
        'custom_config': 'info',
        'greenhouse_connected': 'success'
    }

    return render_template("pages/greenhouse_notification.j2",
                           greenhouse_serial=greenhouse_serial,
                           notifications_kinds=notifications_kinds,
                           sidebar_sensors=sensors.items(),
                           sidebar_actuators=actuators.items(),
                           notifications=get_greenhouse_notifications(greenhouse_serial),
                           notifications_translations=notifications_translations,
                           current_sidebar_item=('notification', None))
