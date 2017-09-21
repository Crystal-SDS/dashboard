class Filter:
    """
        Registry class represents the Registry DSL data
    """

    def __init__(self, dsl_filter_id, name, activation_url, valid_parameters, filter_name):
        self.id = name
        self.name = name
        self.filter_identifier = dsl_filter_id
        self.activation_url = activation_url
        self.valid_parameters = valid_parameters
        self.filter_identifier_name = filter_name
