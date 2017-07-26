import json

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from crystal_dashboard.api import sds_controller as api
from crystal_dashboard.dashboards.sdscontroller.bandwidth_differentiation.proxy_sorting import forms as proxy_sorting_forms


class UploadView(forms.ModalFormView):
    form_class = proxy_sorting_forms.CreateSortedMethod
    form_id = "create_proxy_sorting_form"

    modal_header = _("Create Sort Method")
    submit_label = _("Create Sort Method")
    submit_url = reverse_lazy('horizon:sdscontroller:bandwidth_differentiation:proxy_sorting:upload')
    template_name = "sdscontroller/bandwidth_differentiation/proxy_sorting/upload.html"
    context_object_name = 'proxy_sorting'
    success_url = reverse_lazy('horizon:sdscontroller:bandwidth_differentiation:index')
    page_title = _("Create Sort Method")


class UpdateView(forms.ModalFormView):
    form_class = proxy_sorting_forms.UpdateSortedMethod
    form_id = "update_proxy_sorting_form"
    modal_header = _("Update Sort Method")
    submit_label = _("Update Sort Method")
    submit_url = "horizon:sdscontroller:bandwidth_differentiation:proxy_sorting:update"
    template_name = "sdscontroller/bandwidth_differentiation/proxy_sorting/update.html"
    context_object_name = 'proxy_sorting'
    success_url = reverse_lazy('horizon:sdscontroller:bandwidth_differentiation:index')
    page_title = _("Update Sort Method")

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['proxy_sorting_id'] = self.kwargs['proxy_sorting_id']
        args = (self.kwargs['proxy_sorting_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        proxy_sorting_id = self.kwargs['proxy_sorting_id']
        try:
            proxy_sorting = api.bw_get_sort_method(self.request, proxy_sorting_id)
            return proxy_sorting
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve sorted method details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        proxy_sorting = self._get_object()
        initial = json.loads(proxy_sorting.text)
        return initial
