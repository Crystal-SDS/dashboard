from django import shortcuts
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import messages
from horizon import tables

from crystal_dashboard.api import sds_controller as api
from crystal_dashboard.dashboards.sdscontroller import exceptions as sdsexception

class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class SubmitJob(tables.LinkAction):
    name = "submit"
    verbose_name = _("Submit Job")
    url = "horizon:sdscontroller:analytics_jobs:jobs:submit_job"
    classes = ("ajax-modal",)
    icon = "plus"


class ClearJobs(tables.Action):

    name = "clear"
    verbose_name = "Clear job history"
    verbose_name_plural = verbose_name
    icon = "remove"
    requires_input = False

    def handle(self, data_table, request, obj_ids):
        try:
            response = api.anj_clear_job_history(request)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully cleared history.'))
                return shortcuts.redirect("horizon:sdscontroller:analytics_jobs:index")
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
             redirect = reverse("horizon:sdscontroller:analytics_jobs:index")
             error_message = "Unable to create group.\t %s" % ex.message
             exceptions.handle(request, _(error_message), redirect=redirect)



class JobsTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    job_name = tables.Column('name', verbose_name=_("Job name"))
    pushdown = tables.Column('pushdown', verbose_name=_("Pushdown"))
    timestamp = tables.Column('timestamp', verbose_name=_("Submitted"))
    status = tables.Column('status', verbose_name=_("Status"))

    class Meta:
        name = "jobs"
        verbose_name = _("Jobs")
        table_actions = (MyFilterAction, SubmitJob, ClearJobs )