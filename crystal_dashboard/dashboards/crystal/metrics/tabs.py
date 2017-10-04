import json

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
from crystal_dashboard.api import metrics as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from crystal_dashboard.dashboards.crystal.metrics import models as wm_models
from crystal_dashboard.dashboards.crystal.metrics import tables as wm_tables


class WorkloadMetrics(tabs.TableTab):
    table_classes = (wm_tables.MetricTable,)
    name = _("Workload Metric Modules")
    slug = "metric_modules_table"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_metric_modules_data(self):
        try:
            response = api.get_all_metric_modules(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get metric modules.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = '[]'
            exceptions.handle(self.request, e.message)

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            if inst['execution_server'] == 'proxy':
                inst['execution_server'] = 'Proxy Node'
            elif inst['execution_server'] == 'proxy/object':
                inst['execution_server'] = 'Proxy & Storage Nodes'

            ret.append(wm_models.MetricModule(inst['id'], inst['metric_name'], inst['class_name'], inst['out_flow'], inst['in_flow'],
                                              inst['execution_server'], inst['enabled']))
        return ret


class WorkloadMetricsTabs(tabs.TabGroup):
    slug = "metrics_tabs"
    tabs = (WorkloadMetrics,)
    sticky = True
