import calendar
import time

STATUS_THRESHOLD = 15


class ProxyNode:
    """
        ProxyNode class defines a Swift Proxy node. The identifier is the name of the node.
    """
    def __init__(self, name, ip, region_id, zone_id, ssh_access, last_ping):
        self.id = name
        self.ip = ip
        self.region_id = region_id
        self.zone_id = zone_id
        self.ssh_access = ssh_access
        self.last_ping = last_ping
        self.node_status = calendar.timegm(time.gmtime()) - int(float(last_ping)) <= STATUS_THRESHOLD


class StorageNode:
    """
        StorageNode class defines a Swift storage node. The identifier is the name of the node.
    """
    def __init__(self, name, ip, region_id, zone_id, ssh_access, last_ping, devices):
        self.id = name
        self.ip = ip
        self.region_id = region_id
        self.zone_id = zone_id
        self.ssh_access = ssh_access
        self.last_ping = last_ping
        self.node_status = calendar.timegm(time.gmtime()) - int(float(last_ping)) <= STATUS_THRESHOLD
        self.devices = devices
