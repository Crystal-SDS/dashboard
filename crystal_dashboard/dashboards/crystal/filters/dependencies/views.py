import json

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from crystal_dashboard.api import crystal as api
from crystal_dashboard.dashboards.crystal.filters.dependencies import forms as dependencies_forms


class UploadView(forms.ModalFormView):
    form_class = dependencies_forms.UploadDependency
    form_id = "upload_dependency_form"

    modal_header = _("Upload A Dependency")
    submit_label = _("Upload Dependency")
    submit_url = reverse_lazy('horizon:crystal:filters:dependencies:upload')
    template_name = "crystal/filters/dependencies/upload.html"
    context_object_name = 'dependency'
    success_url = reverse_lazy('horizon:crystal:filters:index')
    page_title = _("Upload A Dependency")


class UpdateView(forms.ModalFormView):
    form_class = dependencies_forms.UpdateDependency
    form_id = "update_dependency_form"
    modal_header = _("Update A Dependency")
    submit_label = _("Update Dependency")
    submit_url = "horizon:crystal:filters:dependencies:update"
    template_name = "crystal/filters/dependencies/update.html"
    context_object_name = 'dependency'
    success_url = reverse_lazy('horizon:crystal:filters:index')
    page_title = _("Update A Dependency")

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['dependency_id'] = self.kwargs['dependency_id']
        args = (self.kwargs['dependency_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        dependency_id = self.kwargs['dependency_id']
        try:
            dependency = api.fil_get_dependency_metadata(self.request, dependency_id)
            return dependency
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve dependency details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        dependency = self._get_object()
        initial = json.loads(dependency.text)
        return initial
