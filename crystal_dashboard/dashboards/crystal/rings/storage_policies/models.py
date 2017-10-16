from __future__ import division


class StoragePolicy:
    """
        Filters class represents the filter data
    """
    def __init__(self, id, name, type, default, parameters, deprecated, deployed, devices):
        self.id = id
        self.name = name
        self.type = type.title()
        self.default = default.title()
        self.parameters = parameters
        self.deprecated = deprecated
        self.deployed = deployed
        self.devices = devices


class Device:

    def __init__(self, id, storage_node, region, zone, device, size_occupied, size):
        self.id = id
        self.storage_node = storage_node
        self.region = region
        self.zone = zone
        self.device = device
        self.size_occupied = str("{0:.1f}".format(size_occupied / (1024*1024*1024))) + 'GB'
        self.size = str("{0:.1f}".format(size / (1024*1024*1024))) + 'GB'
