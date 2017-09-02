import json

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
from crystal_dashboard.api import crystal as api
from crystal_dashboard.dashboards.crystal.sds_policies.metrics import models as metrics_models
from crystal_dashboard.dashboards.crystal.sds_policies.metrics import tables as metrics_tables
from crystal_dashboard.dashboards.crystal.sds_policies.policies import models as policies_models
from crystal_dashboard.dashboards.crystal.sds_policies.policies import tables as policies_tables
from crystal_dashboard.dashboards.crystal.sds_policies.object_types import models as object_types_models
from crystal_dashboard.dashboards.crystal.sds_policies.object_types import tables as object_types_tables


class Policies(tabs.TableTab):
    table_classes = (policies_tables.StaticPoliciesTable, policies_tables.DynamicPoliciesTable,)
    name = _("Policies")
    slug = "policies_table"
    template_name = "crystal/sds_policies/policies/_detail.html"
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
            if self.request.user.project_name == settings.IOSTACK_KEYSTONE_ADMIN_TENANT:
                ret.append(policies_models.StaticPolicy(inst['id'], inst['target_id'], inst['target_name'], inst['filter_name'], inst['object_type'], inst['object_size'], inst['execution_server'], inst['execution_server_reverse'], inst['execution_order'], inst['params']))
            elif self.request.user.project_name == inst['target_name']:
                ret.append(policies_models.StaticPolicy(inst['id'], inst['target_id'], inst['target_name'], inst['filter_name'], inst['object_type'], inst['object_size'], inst['execution_server'], inst['execution_server_reverse'], inst['execution_order'], inst['params']))
        return ret

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
            ret.append(policies_models.DynamicPolicy(inst['id'], inst['policy'], inst['condition'], inst['transient'], inst['policy_location'], inst['alive']))
        return ret


class ObjectTypes(tabs.TableTab):
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


class MetricTab(tabs.TableTab):
    name = _("Activated Workload Metrics")
    slug = "activated_workload_metrics"
    table_classes = (metrics_tables.MetricTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def get_workload_metrics_data(self):
        try:
            response = api.dsl_get_all_workload_metrics(self.request)
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
    tabs = (Policies, ObjectTypes, MetricTab,)
    sticky = True
