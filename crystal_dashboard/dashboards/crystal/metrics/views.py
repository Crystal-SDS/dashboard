import json

from django import http
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon.utils import memoized
from crystal_dashboard.api import metrics as api
from crystal_dashboard.dashboards.crystal.metrics import forms as wm_forms
from crystal_dashboard.dashboards.crystal.metrics import tabs as wm_tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = wm_tabs.WorkloadMetricsTabs
    template_name = 'crystal/metrics/index.html'
    page_title = _("Workload Metrics")

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class UploadView(forms.ModalFormView):
    form_class = wm_forms.UploadMetricModule
    form_id = "upload_metric_module_form"
    modal_header = _("Upload Workload Metric")
    submit_label = _("Upload Workload Metric")
    submit_url = reverse_lazy('horizon:crystal:metrics:upload_metric_module')
    template_name = "crystal/metrics/upload_metric_module.html"
    context_object_name = 'metric_module'
    success_url = reverse_lazy('horizon:crystal:metrics:index')
    page_title = _("Upload Workload Metric")


def download_metric_module(request, metric_module_id):
    try:
        metric_module_response = api.download_metric_module_data(request, metric_module_id)

        # Generate response
        response = http.StreamingHttpResponse(metric_module_response.content)
        response['Content-Disposition'] = metric_module_response.headers['Content-Disposition']
        response['Content-Type'] = metric_module_response.headers['Content-Type']
        response['Content-Length'] = metric_module_response.headers['Content-Length']
        return response

    except Exception as exc:
        redirect = reverse("horizon:crystal:metrics:index")
        exceptions.handle(request, _(exc.message), redirect=redirect)


class UpdateView(forms.ModalFormView):
    form_class = wm_forms.UpdateMetricModule
    form_id = "update_metric_module_form"
    modal_header = _("Update Workload Metric Module")
    submit_label = _("Update Workload Metric")
    submit_url = "horizon:crystal:metrics:update_metric_module"
    template_name = "crystal/metrics/update_metric_module.html"
    context_object_name = 'metric_module'
    success_url = reverse_lazy('horizon:crystal:metrics:index')
    page_title = _("Update Workload Metric Module")

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['metric_module_id'] = self.kwargs['metric_module_id']
        args = (self.kwargs['metric_module_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    # TODO: Change '_get_object' method
    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        metric_module_id = self.kwargs['metric_module_id']
        try:
            metric_module = api.get_metric_module(self.request, metric_module_id)
            return metric_module
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve metric modules details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        metric_module = self._get_object()
        initial = json.loads(metric_module.text)
        return initial


classes = ("ajax-modal",)
