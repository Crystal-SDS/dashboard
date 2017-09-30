class Controller:
    """
        Controllers class models.
    """

    def __init__(self, controller_id, controller_name, description, class_name, enabled):
        self.id = controller_id
        self.controller_name = controller_name
        self.description = description
        self.class_name = class_name
        self.enabled = enabled
