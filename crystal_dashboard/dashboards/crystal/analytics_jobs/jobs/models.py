class Job:
    """
        Job class represents a history Analytics job.
    """

    def __init__(self, id_, name, pushdown, timestamp, status):
        self.id = id_
        self.name = name
        self.pushdown = pushdown
        self.timestamp = timestamp
        self.status = status
