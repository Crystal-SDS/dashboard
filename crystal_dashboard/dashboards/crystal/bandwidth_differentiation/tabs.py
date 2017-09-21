import json

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
from crystal_dashboard.api import crystal as api
from crystal_dashboard.dashboards.crystal import common
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from crystal_dashboard.dashboards.crystal.bandwidth_differentiation.controllers import models as controllers_models
from crystal_dashboard.dashboards.crystal.bandwidth_differentiation.controllers import tables as controllers_tables
from crystal_dashboard.dashboards.crystal.bandwidth_differentiation.proxy_sorting import models as proxy_sorting_models
from crystal_dashboard.dashboards.crystal.bandwidth_differentiation.proxy_sorting import tables as proxy_sorting_tables
from crystal_dashboard.dashboards.crystal.bandwidth_differentiation.slas import models as slas_models
from crystal_dashboard.dashboards.crystal.bandwidth_differentiation.slas import tables as slas_tables


class SLAsTab(tabs.TableTab):
    table_classes = (slas_tables.SLAsTable,)
    name = _("SLOs")
    slug = "slas_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_slas_data(self):
        try:
            response = api.fil_get_all_slos(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get instances.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        # instances = json.loads(strobj)
        # ret = []
        # for inst in instances:
        #     ret.append(slas_models.SLA(inst['project_id'], inst['project_name'], inst['policy_id'], inst['policy_name'], inst['bandwidth']))
        # return ret

        storage_policies_dict = dict(common.get_storage_policy_list(self.request, common.ListOptions.by_id()))
        projects_dict = dict(common.get_project_list(self.request))


        slos = json.loads(strobj)
        tmp_slos = {}
        for slo in slos:
            if slo['dsl_filter'] == 'bandwidth':
                project_target, policy_id = slo['target'].split('#')  # target format is AUTH_X#Y where  X is the project_id and Y is the policy_id
                project_id = project_target.split('_')[1]
                if project_id not in tmp_slos:
                    tmp_slos[project_id] = {}
                if policy_id not in tmp_slos[project_id]:
                    tmp_slos[project_id][policy_id] = {}
                tmp_slos[project_id][policy_id][slo['slo_name']] = slo['value']

        ret = []
        for project_id in tmp_slos.keys():
            for policy_id in tmp_slos[project_id].keys():
                get_bw = tmp_slos[project_id][policy_id]['get_bw']
                put_bw = tmp_slos[project_id][policy_id]['put_bw']
                ssync_bw = tmp_slos[project_id][policy_id]['ssync_bw']
                sla = slas_models.SLA(project_id, projects_dict[str(project_id)], policy_id, storage_policies_dict[str(policy_id)], get_bw, put_bw, ssync_bw)
                ret.append(sla)

        return ret


class ControllersTab(tabs.TableTab):
    table_classes = (controllers_tables.ControllersGETTable, controllers_tables.ControllersPUTTable, controllers_tables.ControllersReplicationTable,)
    name = _("Controllers")
    slug = "controllers_table"
    # template_name = "horizon/common/_detail_table.html"
    template_name = "crystal/bandwidth_differentiation/controllers/_detail.html"
    preload = False
    response = None

    def get_get_controllers_data(self):
        try:
            if not self.response:
                self.response = api.dsl_get_all_global_controllers(self.request)
            if 200 <= self.response.status_code < 300:
                strobj = self.response.text
            else:
                error_message = 'Unable to get instances.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            if inst['dsl_filter'] == 'bandwidth' and inst['type'] == 'get':
                ret.append(controllers_models.Controller(inst['id'], inst['controller_name'], inst['class_name'], inst['enabled']))
        return ret

    def get_put_controllers_data(self):
        try:
            if not self.response:
                self.response = api.dsl_get_all_global_controllers(self.request)
            if 200 <= self.response.status_code < 300:
                strobj = self.response.text
            else:
                error_message = 'Unable to get instances.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            if inst['dsl_filter'] == 'bandwidth' and inst['type'] == 'put':
                ret.append(controllers_models.Controller(inst['id'], inst['controller_name'], inst['class_name'], inst['enabled']))
        return ret

    def get_replication_controllers_data(self):
        try:
            if not self.response:
                self.response = api.dsl_get_all_global_controllers(self.request)
            if 200 <= self.response.status_code < 300:
                strobj = self.response.text
            else:
                error_message = 'Unable to get instances.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            if inst['dsl_filter'] == 'bandwidth' and inst['type'] == 'ssync':
                ret.append(controllers_models.Controller(inst['id'], inst['controller_name'], inst['class_name'], inst['enabled']))
        return ret


class ProxySortingTab(tabs.TableTab):
    table_classes = (proxy_sorting_tables.ProxySortingTable,)
    name = _("Proxy Sorting")
    slug = "proxy_sorting_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_proxy_sorting_data(self):
        try:
            response = api.bw_get_all_sort_method(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get instances.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            ret.append(proxy_sorting_models.ProxySorting(inst['id'], inst['name'], inst['criterion']))
        return ret


class BwDiffTabs(tabs.TabGroup):
    slug = "bandwidth_differentiation_tabs"
    # tabs = (SLAsTab, ProxySortingTab,)
    tabs = (SLAsTab, ControllersTab,)
    sticky = True
