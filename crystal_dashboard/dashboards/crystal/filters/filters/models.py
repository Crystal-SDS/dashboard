class Filter:
    """
    Filters class represents the filter data
    """

    def __init__(self, filter_id, filter_name, dsl_name, filter_type, language, dependencies,
                 interface_version, main, execution_server, reverse, put, get, post, head, delete, valid_parameters):
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
        :param post:
        :param head:
        :param delete:
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
        if put and get and post and head and delete:
            self.methods = 'ALL'
        else: 
            self.methods = (('PUT, ' if put else '') + ('GET, ' if get else '') + ('POST, ' if post else '') + ('HEAD, ' if head else '') + ('DELETE, ' if delete else ''))[0:-2] 
        self.valid_parameters = valid_parameters
