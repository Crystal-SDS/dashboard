
class Zone:
    """
        ProxyNode class defines a Swift Proxy node. The identifier is the name of the node.
    """
    def __init__(self, id_zone, name, region, description):
        self.id = id_zone
        self.name = name
        self.region = region
        self.description = description

