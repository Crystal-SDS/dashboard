class AccessControlPolicy:
    """
        Access Control Policy class models.
    """

    def __init__(self, acl_id, target_id, target_name, user, group, listing, write, read, object_type, object_tag):

        self.id = target_id + ':' + acl_id
        self.target_id = target_id
        self.target_name = target_name
        self.user = user
        self.group = group
        self.write = write
        self.read = read
        self.object_type = object_type
        self.object_tag = object_tag

        self.identity = (('User:  '+user if user else '') + ('Group: '+group if group else ''))

        self.permissions = (('LIST, ' if listing else '') + ('WRITE, ' if write else '') + ('READ, ' if read else ''))[0:-2]

        if read and not object_type and not object_tag:
            self.conditions = 'None; Full Access'
        else:
            self.conditions = (('Object Type: '+object_type+', ' if object_type else '') + ('Object TAG: '+object_tag+', ' if object_tag else ''))[0:-2]
        if not read:
            self.conditions = '-'
