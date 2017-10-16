class AccessControlPolicy:
    """
        Access Control Policy class models.
    """

    def __init__(self, project_id, project_name, policy_id, policy_name, get_bw, put_bw):
        self.id = project_id + '#' + policy_id
        self.project_id = project_id
        self.project_name = project_name
        self.policy_name = policy_name
        self.get_bw = get_bw
        self.put_bw = put_bw
