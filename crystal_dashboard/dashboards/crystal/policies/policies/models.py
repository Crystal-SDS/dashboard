class StaticPolicy:
    """
        StaticPolicy class represents the policy data
    """

    def __init__(self, static_policy_id, target_id, target_name, filter_name,
                 object_name, object_type, object_size, object_tag, execution_server,
                 reverse, execution_order, params, put, get, post, head, delete):
        self.id = target_id + ':' + static_policy_id
        self.target_id = target_id
        self.target_name = target_name
        self.filter_name = filter_name
        self.object_type = object_type
        self.object_size = object_size
        self.object_tag = object_tag
        self.execution_server = execution_server
        self.reverse = reverse
        self.execution_order = execution_order
        self.methods = (('PUT, ' if put else '') + ('GET, ' if get else '') + ('POST, ' if post else '') + ('HEAD, ' if head else '') + ('DELETE, ' if delete else ''))[0:-2]
        self.params = params

        if not object_type and not object_tag and not object_size:
            self.conditions = 'None'
        else:
            self.conditions = (('Object Name: '+object_name+', ' if object_name else '') + ('Object Size: '+object_size+', ' if object_size else '') + ('Object Type: '+object_type+', ' if object_type else '') + ('Object TAG: '+object_tag+', ' if object_tag else ''))[0:-2]


class DynamicPolicy:
    """
        DynamicPolicy class represents the policy data
    """

    def __init__(self, dynamic_policy_id, target_id, target_name, condition,
                 action, filter, object_type, object_size, object_tag, transient,
                 parameters, status):
        self.id = dynamic_policy_id
        self.target_id = target_id
        self.target_name = target_name
        self.condition = condition
        self.action = action
        self.filter = filter
        self.object_type = object_type
        self.object_size = object_size
        self.object_tag = object_tag
        self.transient = transient
        self.parameters = parameters
        self.status = status

        if not object_type and not object_tag and not object_size:
            self.conditions = 'None'
        else:
            self.conditions = (('Object Size: '+object_size+', ' if object_size else '') + ('Object Type: '+object_type+', ' if object_type else '') + ('Object TAG: '+object_tag+', ' if object_tag else ''))[0:-2]

