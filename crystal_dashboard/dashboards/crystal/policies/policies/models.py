class StaticPolicy:
    """
        StaticPolicy class represents the policy data
    """

    def __init__(self, static_policy_id, target_id, target_name, filter_name, object_type, object_size, object_tag, execution_server, reverse, execution_order, params,
                  put, get, post, head, delete,):
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


class DynamicPolicy:
    """
        DynamicPolicy class represents the policy data
    """

    def __init__(self, dynamic_policy_id, target_id, target_name, condition, filter, object_type, object_size, object_tag, transient, alive):
        self.id = dynamic_policy_id
        self.target_id = target_id
        self.target_name = target_name
        self.condition = condition
        self.filter = filter
        self.object_type = object_type
        self.object_size = object_size
        self.object_tag = object_tag
        self.transient = transient
        self.alive = alive
