from flask import session, request, redirect, url_for

from src.database.greenhouse import switch_greenhouse_custom_config
from src.database.plant import (get_plants_greenhouse, actualiaze_greenhouse_targets,
                                add_association_plant, terminate_association)


def plant_manager():
    # TODO:
    #       If the parameter 'is-custom' is True,
    #           the config is specified as post parameters, e.g. 'temperature' = 25
    #           the code should update the greenhouse in the GreenHouses table and switch is_custom_config to true.

    if session.get('is-custom'):
        # Update the GreenHouses table
        switch_greenhouse_custom_config(session['greenhouse_serial]'])
    #       If the parameter 'is-custom' is False,

    #           - the new plants are specified in 'add-plants' as a comma separated list of plant ids.
    #           - the amount of each plant is specified in 'add-plants-count', as a comma separated list of integers
    #             (in the same order ar add-plants).
    #           - the associations to delete are specified in 'remove-associations' as a comma separated list
    #               of ASSOCIATION ids (id of GreenHousePlants). A value can appear multiple times.
    #               If the value appears once while the association contains multiple plants, only one plant is removed.
    #       the code should update the plants in the GreenHousePlants table and switch is_custom_config to false.
    else:
        print(request.args.get('add-plants'))
        print()
        print(request.args.get('add-plants-count'))
        print()
        print(request.args.get('remove-associations'))
        print()
        print(request.args.get('remove-associations-count'))
        # add_association_plant(request.args.get('add_plants'), request.args.get('add_plants_count'))
        # terminate_association(request.args.get('remove_associations'), request.args.get('remove_associations_count'))
        # actualiaze_greenhouse_targets(session['serial'])

        # List of plants ids that were in the greenhouse with start and end date
        return redirect(url_for('greenhouse_plants_page', greenhouse_serial=request.args.get('ghs')))
