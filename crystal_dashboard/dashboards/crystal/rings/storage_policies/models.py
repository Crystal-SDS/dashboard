from __future__ import division


class StorageNode:
    """
        Filters class represents the filter data
    """
    def __init__(self, id, name, type, default, parameters):
        self.id = id
        self.name = name
        self.type = type
        self.default = default
        self.parameters = parameters


class Device:

    def __init__(self, id, storage_node, device, size_occuped, size):
        self.id = id
        self.storage_node = storage_node
        self.device = device
        self.size_occuped = str("{0:.1f}".format(size_occuped / (1024*1024*1024))) + 'GB'
        self.size = str("{0:.1f}".format(size / (1024*1024*1024))) + 'GB'
