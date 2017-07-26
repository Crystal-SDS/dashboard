class StaticPolicy:
    """
        StaticPolicy class represents the policy data
    """

    def __init__(self, static_policy_id, target_id, target_name, filter_name, object_type, object_size, execution_server, execution_server_reverse, execution_order, params):
        self.id = target_id + ':' + static_policy_id
        self.target_id = target_id
        self.target_name = target_name
        self.filter_name = filter_name
        self.object_type = object_type
        self.object_size = object_size
        self.execution_server = execution_server
        self.execution_server_reverse = execution_server_reverse
        self.execution_order = execution_order
        self.params = params


class DynamicPolicy:
    """
        DynamicPolicy class represents the policy data
    """

    def __init__(self, dynamic_policy_id, policy, condition, transient, policy_location, alive):
        self.id = dynamic_policy_id
        self.policy = policy
        self.condition = condition
        self.transient = transient
        self.policy_location = policy_location
        self.alive = alive
