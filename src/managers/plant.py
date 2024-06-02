def plant_manager():
    # TODO:
    #       If the parameter 'is-custom' is True,
    #           the config is specified as post parameters, e.g. 'temperature' = 25
    #           the code should update the greenhouse in the GreenHouses table and switch is_custom_config to true.
    #       If the parameter 'is-custom' is False,
    #           - the new plants are specified in 'add-plants' as a comma separated list of plant ids.
    #           - the amount of each plant is specified in 'add-plants-count', as a comma separated list of integers
    #             (in the same order ar add-plants).
    #           - the associations to delete are specified in 'remove-associations' as a comma separated list
    #               of ASSOCIATION ids (id of GreenHousePlants). A value can appear multiple times.
    #               If the value appears once while the association contains multiple plants, only one plant is removed.
    #       the code should update the plants in the GreenHousePlants table and switch is_custom_config to false.
    pass
