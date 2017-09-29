import json

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
from crystal_dashboard.api import policies as api
from crystal_dashboard.dashboards.crystal import common
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
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
                sla = slas_models.SLA(project_id, projects_dict[str(project_id)], policy_id, storage_policies_dict[str(policy_id)], get_bw, put_bw)
                ret.append(sla)

        return ret


class BwDiffTabs(tabs.TabGroup):
    slug = "bandwidth_differentiation_tabs"
    # tabs = (SLAsTab, ProxySortingTab,)
    tabs = (SLAsTab,)
    sticky = True
