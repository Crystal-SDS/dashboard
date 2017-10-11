from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


from crystal_dashboard.api import controllers as api
import json

from horizon import exceptions
from horizon import forms
from crystal_dashboard.dashboards.crystal.controllers.controllers import forms as controllers_forms


class CreateControllerView(forms.ModalFormView):
    form_class = controllers_forms.CreateController
    form_id = "create_controller_form"

    modal_header = _("Create Controller")
    submit_label = _("Create Controller")
    submit_url = reverse_lazy("horizon:crystal:controllers:controllers:create_controller")
    template_name = "crystal/controllers/controllers/create.html"
    context_object_name = "controller"
    success_url = reverse_lazy("horizon:crystal:controllers:index")
    page_title = _("Create Controller")


class UpdateControllerView(forms.ModalFormView):
    form_class = controllers_forms.UpdateController
    submit_url = "horizon:crystal:controllers:controllers:update_controller"
    form_id = "update_controller_form"
    modal_header = _("Update a Controller")
    submit_label = _("Update Controller")
    template_name = "crystal/controllers/controllers/update.html"
    context_object_name = 'controller'
    success_url = reverse_lazy('horizon:crystal:controllers:index')
    page_title = _("Update a Controller")

    def get_context_data(self, **kwargs):
        context = super(UpdateControllerView, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        args = (self.kwargs['id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def _get_object(self, *args, **kwargs):
        controller_id = self.kwargs['id']
        try:
            filter = api.get_controller(self.request, controller_id)
            return filter
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve controller details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        controller = self._get_object()
        initial = json.loads(controller.text)
        # initial = super(UpdateView, self).get_initial()
        # initial['name'] = "my filter name"
        return initial


class LaunchInstanceView(forms.ModalFormView):
    form_class = controllers_forms.LaunchInstance
    form_id = "launch_instance_form"

    modal_header = _("Launch Instance")
    submit_label = _("Launch Instance")
    submit_url = "horizon:crystal:controllers:controllers:launch_instance"
    template_name = "crystal/controllers/controllers/create.html"
    context_object_name = "controller"
    success_url = reverse_lazy("horizon:crystal:controllers:index")
    page_title = _("Launch Instance")

    def get_context_data(self, **kwargs):
        context = super(LaunchInstanceView, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        args = (self.kwargs['id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def get_initial(self):
        initial = json.loads(api.get_controller(self.request, self.kwargs['id']).text)
        initial['id'] = self.kwargs['id']
        return initial
