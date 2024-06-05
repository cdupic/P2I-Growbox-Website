from flask import session, request, redirect, url_for

from src.database.greenhouse import switch_greenhouse_custom_config
from src.database.plant import (actualiaze_greenhouse_targets,
                                add_association_plant, terminate_association)


def plant_manager():
    # TODO:
    #       If the parameter 'is-custom' is True,
    #           the config is specified as post parameters, e.g. 'temperature' = 25
    #           the code should update the greenhouse in the GreenHouses table and switch is_custom_config to true.

    if session.get('is-custom'):
        # Update the GreenHouses table
        switch_greenhouse_custom_config(request.form.get('ghs'))

    else:
        add_association_plant(session['serial'], [request.form.get('add-plant'), request.form.get('add-plant-count')])
        terminate_association(request.form.get('remove-associations'), request.form.get('remove-associations-count'))
        actualiaze_greenhouse_targets(session['serial'])

        return redirect(url_for('greenhouse_plants_page', greenhouse_serial=request.form.get('ghs')))
