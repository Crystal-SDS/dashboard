from django import http
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

from crystal_dashboard.api import sds_controller as api
from crystal_dashboard.dashboards.sdscontroller.analytics_jobs.analyzers import forms as analyzers_forms


class CreateAnalyzerView(forms.ModalFormView):
    form_class = analyzers_forms.CreateAnalyzer
    modal_header = _("Create Analyzer")
    modal_id = "create_analyzer_modal"
    template_name = 'sdscontroller/analytics_jobs/analyzers/create.html'
    success_url = reverse_lazy('horizon:sdscontroller:analytics_jobs:index')
    page_title = _("Upload an Analyzer")
    submit_label = _("Upload")
    submit_url = reverse_lazy(
        "horizon:sdscontroller:analytics_jobs:analyzers:create_analyzer")

def download_analyzer(request, analyzer_id):
    try:
        analyzer_response = api.anj_download_analyzer(request, analyzer_id)

        # Generate response
        response = http.StreamingHttpResponse(analyzer_response.content)
        response['Content-Disposition'] = analyzer_response.headers['Content-Disposition']
        response['Content-Type'] = analyzer_response.headers['Content-Type']
        response['Content-Length'] = analyzer_response.headers['Content-Length']
        return response

    except Exception as exc:
        redirect = reverse("horizon:sdscontroller:analytics_jobs:index")
        exceptions.handle(request, _(exc.message), redirect=redirect)