import json

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
from crystal_dashboard.api import policies as api
from crystal_dashboard.api import metrics as metrics_api
from crystal_dashboard.dashboards.crystal import common
from crystal_dashboard.dashboards.crystal.policies.metrics import models as metrics_models
from crystal_dashboard.dashboards.crystal.policies.metrics import tables as metrics_tables
from crystal_dashboard.dashboards.crystal.policies.bw_slos import models as bw_slos_models
from crystal_dashboard.dashboards.crystal.policies.bw_slos import tables as bw_slos_tables
from crystal_dashboard.dashboards.crystal.policies.policies import models as policies_models
from crystal_dashboard.dashboards.crystal.policies.policies import tables as policies_tables
from crystal_dashboard.dashboards.crystal.policies.object_types import models as object_types_models
from crystal_dashboard.dashboards.crystal.policies.object_types import tables as object_types_tables
from crystal_dashboard.dashboards.crystal.policies.access_control import models as access_control_models
from crystal_dashboard.dashboards.crystal.policies.access_control import tables as access_control_tables
from openstack_dashboard import api as api_keystone
from openstack_dashboard.utils import identity

from crystal_dashboard.local import local_settings


class StaticPoliciesTab(tabs.TableTab):
    table_classes = (policies_tables.StaticPoliciesTable,)
    name = _("Static Policies")
    slug = "static_policies_table"
    template_name = "crystal/policies/policies/_detail.html"
    preload = False

    def get_static_policies_data(self):
        try:
            response = api.dsl_get_all_static_policies(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to retrieve static_policies information.'
                raise ValueError(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            if inst['execution_server'] == 'proxy':
                inst['execution_server'] = 'Proxy Node'
            elif inst['execution_server'] == 'object':
                inst['execution_server'] = 'Storage Node'
            if inst['reverse'] == 'proxy':
                inst['reverse'] = 'Proxy Node'
            elif inst['reverse'] == 'object':
                inst['reverse'] = 'Storage Node'
            if 'post' not in inst:
                inst['post'] = False
            if 'head' not in inst:
                inst['head'] = False
            if 'delete' not in inst:
                inst['delete'] = False

            if self.request.user.project_name == local_settings.CRYSTAL_ADMIN_PROJECT:
                ret.append(policies_models.StaticPolicy(inst['id'], inst['target_id'], inst['target_name'], inst['filter_name'],
                                                        inst['object_type'], inst['object_size'], inst['object_tag'],
                                                        inst['execution_server'], inst['reverse'], inst['execution_order'], inst['params'],
                                                        inst['put'], inst['get'], inst['post'], inst['head'], inst['delete']))

            elif self.request.user.project_name == inst['target_name'] or inst['target_name'] == 'Global':
                ret.append(policies_models.StaticPolicy(inst['id'], inst['target_id'], inst['target_name'], inst['filter_name'],
                                                        inst['object_type'], inst['object_size'], inst['object_tag'],
                                                        inst['execution_server'], inst['reverse'], inst['execution_order'], inst['params'],
                                                        inst['put'], inst['get'], inst['post'], inst['head'], inst['delete']))
        return ret


class DynamicPoliciesTab(tabs.TableTab):
    table_classes = (policies_tables.DynamicPoliciesTable,)
    name = _("Dynamic Policies")
    slug = "dynamic_policies_table"
    template_name = "crystal/policies/policies/_detail.html"
    preload = False

    def get_dynamic_policies_data(self):
        try:
            response = api.list_dynamic_policies(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to retrieve dynamic_policies information.'
                raise ValueError(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            if self.request.user.project_name == local_settings.CRYSTAL_ADMIN_PROJECT:
                ret.append(policies_models.DynamicPolicy(inst['id'], inst['target_id'], inst['target_name'], inst['condition'], inst['action'], 
                                                         inst['filter'], inst['object_type'], inst['object_size'], inst['object_tag'], inst['transient'], 
                                                         inst['parameters'], inst['status']))
    
            elif self.request.user.project_name == inst['target_name'] or inst['target_name'] == 'Global':
                ret.append(policies_models.DynamicPolicy(inst['id'], inst['target_id'], inst['target_name'], inst['condition'], inst['action'], 
                                                         inst['filter'], inst['object_type'], inst['object_size'], inst['object_tag'], inst['transient'], 
                                                         inst['parameters'], inst['status']))
            
        return sorted(ret, key=lambda x: x.id, reverse=True)


class AccessControlTab(tabs.TableTab):
    table_classes = (access_control_tables.AccessControlTable,)
    name = _("Access Control")
    slug = "access_control_table"
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def get_access_control_policies_data(self):

        ret = []
        try:
            users = [(user.id, user.name) for user in api_keystone.keystone.user_list(self.request)]
            groups = [(group.id, group.name) for group in api_keystone.keystone.group_list(self.request)]
            response = api.access_control_policy_list(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
                instances = json.loads(strobj)
            else:
                error_message = 'Unable to get instances.'
                raise ValueError(error_message)
        except Exception as e:
            instances = []
            users = []
            groups = []
            exceptions.handle(self.request, e.message)

        for inst in instances:
            try:
                if inst['user_id']:
                    inst['user_name'] = [user[1] for user in users if user[0] == inst['user_id']][0]
                else:
                    inst['user_name'] = ''

                if inst['group_id']:
                    inst['group_name'] = [group[1] for group in groups if group[0] == inst['group_id']][0]
                else:
                    inst['group_name'] = ''
            except Exception as e:
                instances = []
                users = []
                exceptions.handle(self.request, "User name not found")
                
            if self.request.user.project_name == local_settings.CRYSTAL_ADMIN_PROJECT:
                ret.append(access_control_models.AccessControlPolicy(inst['id'], inst['target_id'], inst['target_name'],
                                                                 inst['user_name'], inst['group_name'], inst['list'], inst['write'],
                                                                 inst['read'], inst['object_type'], inst['object_tag']))

            elif self.request.user.project_name == inst['target_name'] or inst['target_name'] == 'Global':
                ret.append(access_control_models.AccessControlPolicy(inst['id'], inst['target_id'], inst['target_name'],
                                                                 inst['user_name'], inst['group_name'], inst['list'], inst['write'],
                                                                 inst['read'], inst['object_type'], inst['object_tag']))

        return ret


class SLOsTab(tabs.TableTab):
    table_classes = (bw_slos_tables.SLAsTable,)
    name = _("Bandwidth SLO's")
    slug = "slos_table"
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def get_slas_data(self):
        try:
            response = api.fil_get_all_slos(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get instances.'
                raise ValueError(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        storage_policies_dict = dict(common.get_storage_policy_list(self.request, common.ListOptions.by_id()))
        projects_dict = dict(common.get_project_list(self.request))

        slos = json.loads(strobj)
        tmp_slos = {}
        for slo in slos:
            if slo['dsl_filter'] == 'bandwidth':
                project_target, policy_id = slo['target'].split('#')
                project_id = project_target
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
                sla = bw_slos_models.SLA(project_id, projects_dict[str(project_id)], policy_id, storage_policies_dict[str(policy_id)], get_bw, put_bw)
                ret.append(sla)

        return ret


class ObjectTypesTab(tabs.TableTab):
    table_classes = (object_types_tables.ObjectTypesTable,)
    name = _("Object Types")
    slug = "object_types_table"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_object_types_data(self):
        ret = []
        try:
            response = api.dsl_get_all_object_types(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get object types.'
                raise ValueError(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        object_types = json.loads(strobj)
        for ot in object_types:
            ret.append(object_types_models.ObjectType(ot['name'], ', '.join(ot['types_list'])))
        return ret


class ActivatedMetricsTab(tabs.TableTab):
    name = _("Activated Workload Metrics")
    slug = "activated_workload_metrics"
    table_classes = (metrics_tables.MetricTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def get_workload_metrics_data(self):
        try:
            response = metrics_api.get_activated_workload_metrics(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to retrieve metrics information.'
                raise ValueError(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            ret.append(metrics_models.Metric(inst['name'], inst['network_location'], inst['type']))
        return ret


class PoliciesGroupTabs(tabs.TabGroup):
    slug = "policies_group_tabs"
    tabs = (StaticPoliciesTab, DynamicPoliciesTab, AccessControlTab, SLOsTab, ObjectTypesTab,)
    sticky = True
