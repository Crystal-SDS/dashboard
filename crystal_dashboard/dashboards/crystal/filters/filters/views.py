import json

from django import http
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from crystal_dashboard.api import filters as api
from crystal_dashboard.dashboards.crystal.filters.filters import forms as filters_forms
from crystal_dashboard.dashboards.crystal.filters.filters.models import Filter


class UploadStorletView(forms.ModalFormView):
    form_class = filters_forms.UploadStorletFilter
    form_id = "upload_filter_form"

    modal_header = _("Upload Storlet Filter")
    submit_label = _("Upload Storlet filter")
    submit_url = reverse_lazy('horizon:crystal:filters:filters:upload_storlet')
    template_name = "crystal/filters/filters/upload_storlet.html"
    context_object_name = 'filter'
    success_url = reverse_lazy('horizon:crystal:filters:index')
    page_title = _("Upload Storlet filter")


class UploadNativeView(forms.ModalFormView):
    form_class = filters_forms.UploadNativeFilter
    form_id = "upload_filter_form"

    modal_header = _("Upload Native Filter")
    submit_label = _("Upload Native Filter")
    submit_url = reverse_lazy('horizon:crystal:filters:filters:upload_native')
    template_name = "crystal/filters/filters/upload_native.html"
    context_object_name = 'filter'
    success_url = reverse_lazy('horizon:crystal:filters:index')
    page_title = _("Upload Native Filter")


def download_filter(request, filter_id):
    try:
        filter_response = api.download_filter_data(request, filter_id)

        # Generate response
        response = http.StreamingHttpResponse(filter_response.content)
        response['Content-Disposition'] = filter_response.headers['Content-Disposition']
        response['Content-Type'] = filter_response.headers['Content-Type']
        response['Content-Length'] = filter_response.headers['Content-Length']
        return response

    except Exception as exc:
        redirect = reverse("horizon:crystal:filters:index")
        exceptions.handle(request, _(exc.message), redirect=redirect)


class UpdateView(forms.ModalFormView):
    # form_class = filters_forms.UpdateFilter
    form_id = "update_filter_form"
    modal_header = _("Update A Filter")
    submit_label = _("Update Filter")
    # submit_url = "horizon:crystal:filters:filters:update"
    template_name = "crystal/filters/filters/update.html"
    context_object_name = 'filter'
    success_url = reverse_lazy('horizon:crystal:filters:index')
    page_title = _("Update A Filter")

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['filter_id'] = self.kwargs['filter_id']
        args = (self.kwargs['filter_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        filter_id = self.kwargs['filter_id']
        try:
            filter_data = api.get_filter_metadata(self.request, filter_id)
            return filter_data
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve filter details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        data = self._get_object()
        data = json.loads(data.text)
        return data


class UpdateStorletView(UpdateView):
    form_class = filters_forms.UpdateStorletFilter
    submit_url = "horizon:crystal:filters:filters:update_storlet"


class UpdateNativeView(UpdateView):
    form_class = filters_forms.UpdateNativeFilter
    submit_url = "horizon:crystal:filters:filters:update_native"

classes = ("ajax-modal",)
