from asyncore import write
class AccessControlPolicy:
    """
        Access Control Policy class models.
    """

    def __init__(self, id, project_id, user, write, read, object_type, object_tag):
        
        self.id = id
        self.target_name = project_id
        self.user = user
        self.write = write
        self.read = read
        self.object_type = object_type
        self.object_tag = object_tag
