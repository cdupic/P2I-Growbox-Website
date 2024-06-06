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

        add_plant_list = request.form.get('add-plant').split(',')
        add_count_list = request.form.get('add-plant-count').split(',')
        remove_associations_list = request.form.get('remove-associations').split(',')
        remove_associations_count_list = request.form.get('remove-associations-count').split(',')

        add_association_plant(session['serial'], [add_plant_list, add_count_list])
        terminate_association(remove_associations_list, remove_associations_count_list)
        actualiaze_greenhouse_targets(session['serial'])

        return redirect(url_for('greenhouse_plants_page', greenhouse_serial=request.form.get('ghs')))
