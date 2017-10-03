class Filter:
    """
    Filters class represents the filter data
    """

    def __init__(self, filter_id, filter_name, dsl_name, filter_type, language, dependencies,
                 interface_version, main, execution_server, reverse, put, get):
        """
        :param filter_id:
        :param filter_name:
        :param dsl_name:
        :param filter_type:
        :param language:
        :param dependencies:
        :param interface_version:
        :param main:
        :param execution_server:
        :param reverse:
        :param put:
        :param get:
        """
        self.id = filter_id
        self.filter_name = filter_name
        self.dsl_name = dsl_name
        self.filter_type = filter_type
        self.interface_version = interface_version
        self.dependencies = dependencies
        self.language = language
        self.main = main
        self.execution_server = execution_server
        self.reverse = reverse
        self.put = put
        self.get = get
