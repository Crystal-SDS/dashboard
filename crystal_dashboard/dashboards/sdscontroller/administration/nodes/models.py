import calendar
import time

STATUS_THRESHOLD = 15

class ProxyNode:
    """
        ProxyNode class defines a Swift Proxy node. The identifier is the name of the node.
    """
    def __init__(self, name, ip, last_ping):
        self.id = name
        self.ip = ip
        self.last_ping = last_ping
        self.node_status = calendar.timegm(time.gmtime()) - int(float(last_ping)) <= STATUS_THRESHOLD


class StorageNode:
    """
        StorageNode class defines a Swift storage node. The identifier is the name of the node.
    """
    def __init__(self, name, ip, last_ping, devices):
        self.id = name
        self.ip = ip
        self.last_ping = last_ping
        self.node_status = calendar.timegm(time.gmtime()) - int(float(last_ping)) <= STATUS_THRESHOLD
        self.devices = devices
