class StaticPolicy:
    """
        StaticPolicy class represents the policy data
    """

    def __init__(self, static_policy_id, target_id, target_name, filter_name, object_type, object_size, object_tag, execution_server, reverse, execution_order, params):
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
        self.params = params


class DynamicPolicy:
    """
        DynamicPolicy class represents the policy data
    """

    def __init__(self, dynamic_policy_id, target, condition, filter, object_type, object_size, object_tag, transient, policy, alive):
        self.id = dynamic_policy_id
        self.target = target
        self.condition = condition
        self.filter = filter
        self.object_type = object_type
        self.object_size = object_size
        self.object_tag = object_tag
        self.transient = transient
        self.policy = policy
        self.alive = alive
