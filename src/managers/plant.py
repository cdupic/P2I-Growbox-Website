from flask import session, render_template

from src.database.greenhouse import switch_greenhouse_custom_config
from src.database.plant import add_association_plant, terminate_association
from src.database.greenhouse import get_dic_users_role_greenhouse, get_greenhouse_name
from src.database.measure import get_sensors_greenhouse, get_actuators_greenhouse
from src.database.plant import get_plants_greenhouse, get_data_plant, get_history_greenhouse



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


        # add_association_plant(request.args.get('add_plants'), request.args.get('add_plants_count'))
        # terminate_association(request.args.get('remove_associations'), request.args.get('remove_associations_count'))
        greenhouse_serial = session['serial']
        current_plants = get_plants_greenhouse(greenhouse_serial)
        id_plants = [current_plants[plant][0] for plant in current_plants]
        nb_distinct_plants = len(set(id_plants))
        nb_crops = sum([current_plants[plant][1] for plant in current_plants])

        # List of plants ids that were in the greenhouse with start and end date
        # old_plants = {association_id: (plant_id, plant_name, count, start_date, end_date)}
        return render_template('pages/greenhouse_plants.j2',
                               current_sidebar_item=('plants', None),
                               greenhouse_serial=greenhouse_serial,
                               greenhouse_name=get_greenhouse_name(greenhouse_serial, session['user_name']),
                               sidebar_sensors=get_sensors_greenhouse(greenhouse_serial).items(),
                               sidebar_actuators=get_actuators_greenhouse(greenhouse_serial).items(),
                               sidebar_users=get_dic_users_role_greenhouse(greenhouse_serial).items(),

                               available_plants=get_data_plant(),
                               old_plants=get_history_greenhouse(greenhouse_serial),
                               current_plants=get_plants_greenhouse(greenhouse_serial),

                               nb_distinct_plants=nb_distinct_plants,
                               nb_crops=nb_crops)
