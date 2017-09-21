import json

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
from crystal_dashboard.api import crystal as api
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
                try:
                    region_name = json.loads(api.get_region(self.request, node['region_id']).text)['name']
                    zone_name = json.loads(api.get_zone(self.request, node['zone_id']).text)['name']
                except Exception as e:
                    region_name = 'Unknown'
                    zone_name = 'Unknown'
                ret.append(nodes_models.ProxyNode(node['name'], node['ip'], region_name, zone_name, node['ssh_access'], node['last_ping']))
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
                try:
                    region_name = json.loads(api.get_region(self.request, node['region_id']).text)['name']
                    zone_name = json.loads(api.get_zone(self.request, node['zone_id']).text)['name']
                except Exception as e:
                    region_name = 'Unknown'
                    zone_name = 'Unknown'
                ret.append(nodes_models.StorageNode(node['name'], node['ip'], region_name, zone_name, node['ssh_access'], node['last_ping'], node['devices']))
        return ret


class NodesTabs(tabs.TabGroup):
    slug = "nodes_tabs"
    tabs = (Nodes,)
    sticky = True
