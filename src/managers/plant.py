from flask import session, request, redirect, url_for

from src.database.greenhouse import get_role_user, set_custom_config_greenhouse
from src.database.plant import (actualiaze_greenhouse_targets,
                                add_association_plant, terminate_association)


def plant_manager():
    if get_role_user(request.form.get('ghs'), session['user_name']) != 'guest':
        if request.form.get('action') == 'custom':
            set_custom_config_greenhouse(request.form.get('ghs'), request.form.get('temperature'),
                                         request.form.get('soil_humidity'), request.form.get('air_humidity'),
                                         request.form.get('light'))

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

    else:
        session['error'] = "Vous n'avez pas les permissions nécessaires pour effectuer cette action."

    return redirect(url_for('greenhouse_plants_page', greenhouse_serial=request.form.get('ghs')))
