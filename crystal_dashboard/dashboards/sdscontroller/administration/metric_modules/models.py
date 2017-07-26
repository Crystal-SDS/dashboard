class MetricModule:
    """
        Metric Module class represents the metric module data
    """

    def __init__(self, metric_module_id, metric_name, class_name, out_flow, in_flow, execution_server, enabled):
        """

        :param metric_module_id:
        :param metric_name:
        :param class_name:
        :param out_flow:
        :param in_flow:
        :param execution_server:
        :param enabled
        """
        self.id = metric_module_id
        self.metric_name = metric_name
        self.class_name = class_name
        self.out_flow = out_flow
        self.in_flow = in_flow
        self.execution_server = execution_server
        self.enabled = enabled
