class AccessControlPolicy:
    """
        Access Control Policy class models.
    """

    def __init__(self, acl_id, target_id, target_name, user, write, read, object_type, object_tag):

        self.id = target_id + ':' + acl_id
        self.target_id = target_id
        self.target_name = target_name
        self.user = user
        self.write = write
        self.read = read
        self.object_type = object_type
        self.object_tag = object_tag
