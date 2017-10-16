import json

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from crystal_dashboard.api import policies as api
from crystal_dashboard.dashboards.crystal.policies.access_control import forms as ac_forms


class CreateView(forms.ModalFormView):
    form_class = ac_forms.CreateAccessControlPolicy
    form_id = "create_access_control_policy_form"

    modal_header = _("Create a Policy")
    submit_label = _("Create Policy")
    submit_url = reverse_lazy("horizon:crystal:policies:access_control:create")
    template_name = "crystal/policies/access_control/create.html"
    context_object_name = "access_control"
    success_url = reverse_lazy("horizon:crystal:policies:index")
    page_title = _("Create a Policy")


class UpdateView(forms.ModalFormView):
    form_class = ac_forms.UpdateAccessControlPolicy
    form_id = "update_access_control_policy_form"
    modal_header = _("Update a Policy")
    submit_label = _("Update Policy")
    submit_url = "horizon:crystal:policies:access_control:update"
    template_name = "crystal/policies/access_control/update.html"
    context_object_name = "access_control"
    success_url = reverse_lazy("horizon:crystal:policies:index")
    page_title = _("Update a Policy")

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context["policy_id"] = self.kwargs["policy_id"]
        args = (self.kwargs["policy_id"],)
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
            msg = _("Unable to retrieve policy details.")
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        # sla = self._get_object()
        # initial = json.loads(sla.text)
        # return initial
        return self._get_object()
