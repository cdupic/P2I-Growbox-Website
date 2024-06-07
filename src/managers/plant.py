from flask import session, request, redirect, url_for

from src.database.greenhouse import switch_greenhouse_custom_config
from src.database.plant import (actualiaze_greenhouse_targets,
                                add_association_plant, terminate_association)


def plant_manager():
    print(request.form)
    if request.form.get('action') == 'custom':

        switch_greenhouse_custom_config(request.form.get('ghs'))
        session['success'] = "Les modifications ont bien été prises en compte."

    elif request.form.get('action') == 'plant':

        add_plant_list = request.form.get('add-plant').split(',')
        add_count_list = request.form.get('add-plant-count').split(',')
        remove_associations_list = request.form.get('remove-associations').split(',')
        remove_associations_count_list = request.form.get('remove-associations-count').split(',')

        add_association_plant(request.form.get('ghs'), [add_plant_list, add_count_list])
        terminate_association(remove_associations_list, remove_associations_count_list)
        actualiaze_greenhouse_targets(request.form.get('ghs'))

        session['success'] = "Les modifications ont bien été prises en compte."

    else:
        session['error'] = "Une erreur s'est produite lors de la modification de la configuration de la serre."

    return redirect(url_for('greenhouse_plants_page', greenhouse_serial=request.form.get('ghs')))
