from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from horizon import exceptions
from horizon import forms
import json
from crystal_dashboard.dashboards.crystal.controllers.instances import forms as instances_forms
from crystal_dashboard.api import controllers as api


class CreateInstanceView(forms.ModalFormView):
    form_class = instances_forms.CreateInstance
    form_id = "create_instance_form"

    modal_header = _("Create Instance")
    submit_label = _("Create Instance")
    submit_url = reverse_lazy("horizon:crystal:controllers:instances:create_instance")
    template_name = "crystal/controllers/instances/create.html"
    context_object_name = "instance"
    success_url = reverse_lazy("horizon:crystal:controllers:index")
    page_title = _("Create Instance")


class UpdateInstanceView(forms.ModalFormView):
    form_class = instances_forms.UpdateInstance
    submit_url = "horizon:crystal:controllers:instances:update_instance"
    form_id = "update_instance_form"
    modal_header = _("Update an Instance")
    submit_label = _("Update Instance")
    template_name = "crystal/controllers/instances/update.html"
    context_object_name = 'instance'
    success_url = reverse_lazy('horizon:crystal:controllers:index')
    page_title = _("Update an Instance")

    def get_context_data(self, **kwargs):
        context = super(UpdateInstanceView, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        args = (self.kwargs['id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def _get_object(self, *args, **kwargs):
        instance_id = self.kwargs['id']
        try:
            instance = api.get_instance(self.request, instance_id)
            return instance
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve instance details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        instance = self._get_object()
        initial = json.loads(instance.text)
        initial['id'] = self.kwargs['id']
        return initial
