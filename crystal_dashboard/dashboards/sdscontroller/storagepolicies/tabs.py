import json

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller.storagepolicies.metrics import models as metrics_models
from openstack_dashboard.dashboards.sdscontroller.storagepolicies.metrics import tables as metrics_tables
from openstack_dashboard.dashboards.sdscontroller.storagepolicies.policies import models as policies_models
from openstack_dashboard.dashboards.sdscontroller.storagepolicies.policies import tables as policies_tables


class Policies(tabs.TableTab):
    table_classes = (policies_tables.StaticPoliciesTable, policies_tables.DynamicPoliciesTable,)
    name = _("Policies")
    slug = "policies_table"
    template_name = "sdscontroller/storagepolicies/policies/_detail.html"
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


class MetricTab(tabs.TableTab):
    name = _("Workload Metric Tab")
    slug = "workload_metric_tab"
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
    tabs = (Policies, MetricTab,)
    sticky = True
