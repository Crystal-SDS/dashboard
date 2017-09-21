class Dependency:
    """
        Dependency class represents the Projects in the System
    """

    def __init__(self, id, name, version, permissions):
        self.id = id
        self.name = name
        self.version = version
        self.permissions = permissions
