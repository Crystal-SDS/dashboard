from crystal_dashboard.dashboards.crystal.regions import tables as region_tables
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from horizon import tables
from horizon import forms
from horizon import exceptions
from horizon.utils import memoized

from django.core.urlresolvers import reverse
from crystal_dashboard.dashboards.crystal.regions import forms as region_forms
from crystal_dashboard.api import swift as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from crystal_dashboard.dashboards.crystal.regions.models import Region
import json


class IndexView(tables.DataTableView):
    # A very simple class-based view...
    table_class = region_tables.RegionsTable
    template_name = "crystal/regions/index.html"
    page_title = _("Regions")

    def get_data(self):

        ret = []
        try:
            response = api.swift_list_regions(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get regions.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = '[]'
            exceptions.handle(self.request, e.message)

        regions = json.loads(strobj)
        for region in regions:
            ret.append(Region(region['id'], region['name'], region['description']))
        return ret


class CreateRegion(forms.ModalFormView):
    form_class = region_forms.CreateRegion
    form_id = "create_region_form"

    modal_header = _("Create a Region")
    submit_label = _("Create Region")
    submit_url = reverse_lazy('horizon:crystal:regions:create')
    template_name = "crystal/regions/create_region.html"
    context_object_name = 'create_region'
    success_url = reverse_lazy('horizon:crystal:regions:index')
    page_title = _("Create a region")


class UpdateRegion(forms.ModalFormView):
    form_class = region_forms.UpdateRegion
    form_id = "update_region_form"
    modal_header = _("Update a Region")
    submit_label = _("Update Region")
    submit_url = "horizon:crystal:regions:update"
    template_name = "crystal/regions/update_region.html"
    context_object_name = 'region'
    success_url = reverse_lazy('horizon:crystal:regions:index')
    page_title = _("Update a Region")

    def get_context_data(self, **kwargs):
        context = super(UpdateRegion, self).get_context_data(**kwargs)
        args = (self.kwargs['region_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        region_id = self.kwargs['region_id']
        try:
            region = api.get_region(self.request, region_id)
            return region
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve region details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        region = self._get_object()
        region_json = json.loads(region.text)
        region_json['region_id'] = self.kwargs['region_id']
        return region_json
