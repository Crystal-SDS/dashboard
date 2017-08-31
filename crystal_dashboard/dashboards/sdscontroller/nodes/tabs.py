import json

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
from crystal_dashboard.api import crystal as api
from crystal_dashboard.dashboards.sdscontroller import exceptions as sdsexception
from crystal_dashboard.dashboards.sdscontroller.nodes import models as nodes_models
from crystal_dashboard.dashboards.sdscontroller.nodes import tables as nodes_tables


class Nodes(tabs.TableTab):
    table_classes = (nodes_tables.ProxysTable, nodes_tables.StorageNodesTable,)
    name = _("Nodes")
    slug = "nodes_table"
    template_name = "sdscontroller/nodes/_detail.html"
    preload = False

    def get_proxys_data(self):
        ret = []
        try:
            response = api.swift_get_all_nodes(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get nodes.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = '[]'
            exceptions.handle(self.request, e.message)

        nodes = json.loads(strobj)
        for node in nodes:
            if node['type'] == 'proxy':
                ret.append(nodes_models.ProxyNode(node['name'], node['ip'], node['last_ping']))
        return ret

    def get_storagenodes_data(self):
        ret = []
        try:
            response = api.swift_get_all_nodes(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get nodes.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = '[]'
            exceptions.handle(self.request, e.message)

        nodes = json.loads(strobj)
        for node in nodes:
            if node['type'] == 'object':
                ret.append(nodes_models.StorageNode(node['name'], node['ip'], node['last_ping'], node['devices']))
        return ret


class NodesTabs(tabs.TabGroup):
    slug = "nodes_tabs"
    tabs = (Nodes,)
    sticky = True
