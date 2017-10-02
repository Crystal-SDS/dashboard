class CrystalProject:
    """
    Project to use for crystal
    """

    def __init__(self, project_id, project_name, description, domain_name, enabled, crystal_enabled):
        """

        :param project_id: project id
        :param project_name: project name
        :param description: project description
        :param domain_name: domain name
        :param enabled: project enabled in swift
        :param crystal_enabled: project enabled in crystal
        """
        self.id = project_id
        self.name = project_name
        self.description = description
        self.domain_name = domain_name
        self.enabled = enabled
        self.crystal_enabled = crystal_enabled
