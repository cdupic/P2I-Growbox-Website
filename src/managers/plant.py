from flask import session, redirect, url_for, request, render_template


def plant_manager():
    # TODO:
    #       If the parameter 'is_custom' is True,
    #           the config is specified as post parameters, e.g. 'temperature' = 25
    #           the code should update the greenhouse in the GreenHouses table and switch is_custom_config to true.
    #       If the parameter 'is_custom' is False,
    #           the new plants are specified in 'new_plants' as a comma separated list of plant ids.
    #           the plants to delete are specified in 'remove_plants' as a comma separated list
    #               of ASSOCIATION ids (id of GreenHousePlants).
    #       the code should update the plants in the GreenHousePlants table and switch is_custom_config to false.
    pass
