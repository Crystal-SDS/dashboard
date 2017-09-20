from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import exceptions
from horizon import tables

from crystal_dashboard.api import sds_controller as api
from crystal_dashboard.dashboards.sdscontroller import exceptions as sdsexception

class MyFilterAction(tables.FilterAction):
    name = "myfilter"

class CreateAnalyzer(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Analyzer")
    url = "horizon:sdscontroller:analytics_jobs:analyzers:create_analyzer"
    classes = ("ajax-modal",)
    icon = "plus"


class DownloadAnalyzer(tables.LinkAction):
    name = "download"
    verbose_name = _("Download")
    icon = "download"

    def get_link_url(self, datum=None):
        base_url = reverse('horizon:sdscontroller:analytics_jobs:analyzers:download_analyzer', kwargs={'analyzer_id': datum.id})
        return base_url


class DeleteAnalyzer(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Analyzer",
            u"Delete Analyzers",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Analyzer",
            u"Deleted Analyzers",
            count
        )

    name = "delete_analyzer"
    success_url = "horizon:sdscontroller:analytics_jobs:index"

    def delete(self, request, obj_id):
        try:
            response = api.anj_delete_analyzer(request, obj_id)
            if 200 <= response.status_code < 300:
                pass
                # messages.success(request, _('Successfully deleted analyzer: %s') % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:analytics_jobs:index")
            error_message = "Unable to remove analyzer.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class AnalyzersTable(tables.DataTable):
    # id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    framework = tables.Column('framework', verbose_name=_("Framework"))
    job_language = tables.Column('job_language', verbose_name=_("Job language"))

    class Meta:
        name = "analyzers"
        verbose_name = _("Analyzers")
        table_actions = (MyFilterAction, CreateAnalyzer)
        row_actions = (DownloadAnalyzer, DeleteAnalyzer,)