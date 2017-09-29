import json

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
from crystal_dashboard.api import swift as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from crystal_dashboard.dashboards.crystal.nodes import models as nodes_models
from crystal_dashboard.dashboards.crystal.nodes import tables as nodes_tables


class Nodes(tabs.TableTab):
    table_classes = (nodes_tables.ProxysTable, nodes_tables.StorageNodesTable,)
    name = _("Nodes")
    slug = "nodes_table"
    template_name = "crystal/nodes/_detail.html"
    response = None

    def get_proxys_data(self):
        ret = []
        try:
            if not self.response:
                self.response = api.swift_get_all_nodes(self.request)
            if 200 <= self.response.status_code < 300:
                strobj = self.response.text
            else:
                error_message = 'Unable to get nodes.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = '[]'
            exceptions.handle(self.request, e.message)

        nodes = json.loads(strobj)
        for node in nodes:
            if node['type'] == 'proxy':
                ret.append(nodes_models.ProxyNode(node['name'], node['ip'], node['region_name'], node['zone_name'], node['ssh_access'], node['last_ping']))
        return ret

    def get_storagenodes_data(self):
        ret = []
        try:
            if not self.response:
                self.response = api.swift_get_all_nodes(self.request)
            if 200 <= self.response.status_code < 300:
                strobj = self.response.text
            else:
                error_message = 'Unable to get nodes.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = '[]'
            exceptions.handle(self.request, e.message)

        nodes = json.loads(strobj)
        for node in nodes:
            if node['type'] == 'object':
                ret.append(nodes_models.StorageNode(node['name'], node['ip'], node['region_name'], node['zone_name'], node['ssh_access'], node['last_ping'], node['devices']))
        return ret


class NodesTabs(tabs.TabGroup):
    slug = "nodes_tabs"
    tabs = (Nodes,)
    sticky = True
