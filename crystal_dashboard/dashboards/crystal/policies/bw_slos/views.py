import json

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from crystal_dashboard.api import policies as api
from crystal_dashboard.dashboards.crystal.policies.bw_slos import forms as slos_forms


class CreateView(forms.ModalFormView):
    form_class = slos_forms.CreateSLA
    form_id = "create_slo_form"

    modal_header = _("Create an SLO")
    submit_label = _("Create SLO")
    submit_url = reverse_lazy("horizon:crystal:policies:bw_slos:create")
    template_name = "crystal/policies/bw_slos/create.html"
    context_object_name = "slo"
    success_url = reverse_lazy("horizon:crystal:policies:index")
    page_title = _("Create a SLO")


class UpdateView(forms.ModalFormView):
    form_class = slos_forms.UpdateSLA
    form_id = "update_slo_form"
    modal_header = _("Update an SLO")
    submit_label = _("Update SLO")
    submit_url = "horizon:crystal:policies:bw_slos:update"
    template_name = "crystal/policies/bw_slos/update.html"
    context_object_name = "slo"
    success_url = reverse_lazy("horizon:crystal:policies:index")
    page_title = _("Update an SLO")

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context["slo_id"] = self.kwargs["slo_id"]
        args = (self.kwargs["slo_id"],)
        context["submit_url"] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        slo_id = self.kwargs["slo_id"]
        try:
            get_sla = api.fil_get_slo(self.request, 'bandwidth', 'get_bw', slo_id)
            put_sla = api.fil_get_slo(self.request, 'bandwidth', 'put_bw', slo_id)

            obj = {"id": slo_id,
                   "get_bandwidth": json.loads(get_sla.text)['value'],
                   "put_bandwidth": json.loads(put_sla.text)['value']}
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
