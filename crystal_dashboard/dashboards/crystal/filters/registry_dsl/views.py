import json

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from crystal_dashboard.api import crystal as api
from crystal_dashboard.dashboards.crystal.filters.registry_dsl import forms as policies_forms


class CreateFilterView(forms.ModalFormView):
    form_class = policies_forms.CreateFilter
    modal_header = _("Register Filter")
    modal_id = "create_filter_modal"
    template_name = 'crystal/filters/registry_dsl/create_filter.html'
    success_url = reverse_lazy('horizon:crystal:filters:index')
    page_title = _("Register a Filter")
    submit_label = _("Register")
    submit_url = reverse_lazy(
        "horizon:crystal:filters:registry_dsl:create_filter")


class UpdateFilterView(forms.ModalFormView):
    form_class = policies_forms.UpdateFilter
    form_id = "update_filter_form"
    modal_header = _("Update A Filter")
    submit_label = _("Update Filter")
    submit_url = "horizon:crystal:filters:registry_dsl:update_filter"
    template_name = "crystal/filters/registry_dsl/update_filter.html"
    context_object_name = 'filter'
    success_url = reverse_lazy('horizon:crystal:filters:index')
    page_title = _("Update A Filter")

    def get_context_data(self, **kwargs):
        context = super(UpdateFilterView, self).get_context_data(**kwargs)
        context['name'] = self.kwargs['name']
        args = (self.kwargs['name'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        name = self.kwargs['name']
        try:
            filter = api.dsl_get_filter_metadata(self.request, name)
            return filter
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve filter details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        filter = self._get_object()
        name = self.kwargs['name']
        initial = json.loads(filter.text)
        initial['name'] = name
        print(initial)
        return initial
