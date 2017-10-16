class Group:
    """
        Group class represents the tenants group in the System
    """

    def __init__(self, id_, name, projects):
        self.id = id_
        self.name = name
        self.projects = projects
