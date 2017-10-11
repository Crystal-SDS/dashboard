class Instance:
    """
        Instances class models.
    """

    def __init__(self, instance_id, controller, parameters, description, status):
        self.id = instance_id
        self.controller = controller
        self.parameters = parameters
        self.description = description
        self.status = status
