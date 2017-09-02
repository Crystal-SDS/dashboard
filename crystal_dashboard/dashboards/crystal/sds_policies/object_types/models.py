class ObjectType:
    """
        ObjectType class defines a group of objects to which a policy can be applied. The id of the ObjectType can
        be used in a DSL policy definition.
    """
    def __init__(self, id, extensions):
        self.id = id
        self.extensions = extensions
