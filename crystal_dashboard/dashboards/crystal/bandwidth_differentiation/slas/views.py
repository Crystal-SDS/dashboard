import json

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from crystal_dashboard.api import crystal as api
from crystal_dashboard.dashboards.crystal.bandwidth_differentiation.slas import forms as slas_forms


class CreateView(forms.ModalFormView):
    form_class = slas_forms.CreateSLA
    form_id = "create_sla_form"

    modal_header = _("Create an SLO")
    submit_label = _("Create SLO")
    submit_url = reverse_lazy("horizon:crystal:bandwidth_differentiation:slas:create_sla")
    template_name = "crystal/bandwidth_differentiation/slas/create.html"
    context_object_name = "sla"
    success_url = reverse_lazy("horizon:crystal:bandwidth_differentiation:index")
    page_title = _("Create A SLA")


class UpdateView(forms.ModalFormView):
    form_class = slas_forms.UpdateSLA
    form_id = "update_sla_form"
    modal_header = _("Update an SLO")
    submit_label = _("Update SLO")
    submit_url = "horizon:crystal:bandwidth_differentiation:slas:update_sla"
    template_name = "crystal/bandwidth_differentiation/slas/update.html"
    context_object_name = "sla"
    success_url = reverse_lazy("horizon:crystal:bandwidth_differentiation:index")
    page_title = _("Update an SLO")

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context["sla_id"] = self.kwargs["sla_id"]
        args = (self.kwargs["sla_id"],)
        context["submit_url"] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        sla_id = self.kwargs["sla_id"]
        try:
            get_sla = api.fil_get_slo(self.request, 'bandwidth', 'get_bw', sla_id)
            put_sla = api.fil_get_slo(self.request, 'bandwidth', 'put_bw', sla_id)
            ssync_sla = api.fil_get_slo(self.request, 'bandwidth', 'ssync_bw', sla_id)

            obj = {"id": sla_id,
                   "get_bandwidth": json.loads(get_sla.text)['value'],
                   "put_bandwidth": json.loads(put_sla.text)['value'],
                   "ssync_bandwidth": json.loads(ssync_sla.text)['value']}
            return obj

        except Exception:
            redirect = self.success_url
            msg = _("Unable to retrieve SLO details.")
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        # sla = self._get_object()
        # initial = json.loads(sla.text)
        # return initial
        return self._get_object()
