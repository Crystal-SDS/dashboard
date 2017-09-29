class Controller:
    """
        Controllers class models.
    """

    def __init__(self, controller_id, controller_name, class_name, enabled):
        self.id = controller_id
        self.controller_name = controller_name
        self.class_name = class_name
        self.enabled = enabled
