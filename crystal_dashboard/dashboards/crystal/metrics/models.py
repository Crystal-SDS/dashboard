class MetricModule:
    """
        Metric Module class represents the metric module data
    """

    def __init__(self, metric_module_id, metric_name, class_name, put, get, ssync, execution_server, status):
        """

        :param metric_module_id:
        :param metric_name:
        :param class_name:
        :param out_flow:
        :param in_flow:
        :param ssync:
        :param execution_server:
        :param status
        """
        self.id = metric_module_id
        self.metric_name = metric_name
        self.class_name = class_name
        self.methods = (('PUT, ' if put else '') + ('GET, ' if get else '') + ('SSYNC, ' if ssync else ''))[0:-2]
        self.execution_server = execution_server
        self.status = status
