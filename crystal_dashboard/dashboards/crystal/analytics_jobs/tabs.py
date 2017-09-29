import json

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
from crystal_dashboard.api import sds_controller as api
from crystal_dashboard.dashboards.sdscontroller import exceptions as sdsexception

from crystal_dashboard.dashboards.sdscontroller.analytics_jobs.jobs import models as job_models
from crystal_dashboard.dashboards.sdscontroller.analytics_jobs.jobs import tables as job_tables
from crystal_dashboard.dashboards.sdscontroller.analytics_jobs.analyzers import models as analyzer_models
from crystal_dashboard.dashboards.sdscontroller.analytics_jobs.analyzers import tables as analyzer_tables


class JobsTab(tabs.TableTab):
    table_classes = (job_tables.JobsTable,)
    name = _("Jobs")
    slug = "jobs_table"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_jobs_data(self):
        ret = []
        try:
            response = api.anj_list_job_history(self.request)  # TODO Change
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get jobs.'
                raise sdsexception.SdsException(error_message)

        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        jobs = json.loads(strobj)
        for j in jobs:
            ret.append(job_models.Job(j['id'], j['name'], j['pushdown'], j['timestamp'], j['status']))
        return ret


class AnalyzersTab(tabs.TableTab):
    table_classes = (analyzer_tables.AnalyzersTable,)
    name = _("Analyzers")
    slug = "analyzers_table"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_analyzers_data(self):
        ret = []
        try:
            response = api.anj_list_analyzers(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get analyzers.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        analyzers = json.loads(strobj)
        for a in analyzers:
            ret.append(analyzer_models.Analyzer(a['id'], a['name'], a['framework'], a['job_language']))
        return ret


class MyPanelTabs(tabs.TabGroup):
    slug = "mypanel_tabs"
    tabs = (JobsTab, AnalyzersTab,)
    sticky = True