import json

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from crystal_dashboard.api import policies as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
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

    def _get_object(self, *args, **kwargs):
        acl_id = self.kwargs["policy_id"]
        try:
            response = api.get_access_control_policy(self.request, acl_id)
            if 200 > response.status_code >= 300:
                raise sdsexception.SdsException(response.text)
            else:
                return json.loads(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:policies:index")
            error_message = "Unable to update ACL.\t %s" % ex.message
            exceptions.handle(self.request, _(error_message), redirect=redirect)

    def get_initial(self):
        initial = self._get_object()
        initial['policy_id'] = self.kwargs["policy_id"]
        return initial
