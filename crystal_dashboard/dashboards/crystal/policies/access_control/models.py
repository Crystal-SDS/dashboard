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

        self.permissions = (('WRITE, ' if write else '') + ('READ, ' if read else ''))[0:-2]

        if (not object_type and not object_tag) or not read:
            self.conditions = 'None; Full Access'
        else:
            self.conditions = (('Object Type: '+object_type+', ' if object_type else '') + ('Object TAG: '+object_tag+', ' if object_tag else ''))[0:-2]
