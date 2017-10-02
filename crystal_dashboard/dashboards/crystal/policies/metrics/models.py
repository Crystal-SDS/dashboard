class Metric:
    """
        Policy class represents the policy data
    """
    def __init__(self, name, network_location, metric_type):
        self.id = name
        self.network_location = network_location
        self.type = metric_type
