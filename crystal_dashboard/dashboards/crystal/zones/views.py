from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from horizon import tables
from horizon import forms
from horizon import exceptions
from horizon.utils import memoized
from django.core.urlresolvers import reverse

from crystal_dashboard.dashboards.crystal.zones import forms as zone_forms
from crystal_dashboard.dashboards.crystal.zones import tables as zone_tables
from crystal_dashboard.api import swift as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from crystal_dashboard.dashboards.crystal.zones.models import Zone
import json


class IndexView(tables.DataTableView):
    # A very simple class-based view...
    table_class = zone_tables.ZonesTable
    template_name = "crystal/zones/index.html"
    page_title = _("Zones")

    def get_data(self):

        ret = []
        try:
            response = api.swift_list_zones(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get zones.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = '[]'
            exceptions.handle(self.request, e.message)

        zones = json.loads(strobj)
        for zone in zones:
            ret.append(Zone(zone['id'], zone['name'], zone['region_name'], zone['description']))

        return ret


class CreateZone(forms.ModalFormView):
    form_class = zone_forms.CreateZone
    form_id = "create_zone_form"

    modal_header = _("Create a Zone")
    submit_label = _("Create Zone")
    submit_url = reverse_lazy('horizon:crystal:zones:create')
    template_name = "crystal/zones/create_zone.html"
    context_object_name = 'create_zone'
    success_url = reverse_lazy('horizon:crystal:zones:index')
    page_title = _("Create a zone")


class UpdateZone(forms.ModalFormView):
    form_class = zone_forms.UpdateZone
    form_id = "update_zone_form"
    modal_header = _("Update a Zone")
    submit_label = _("Update Zone")
    submit_url = "horizon:crystal:zones:update"
    template_name = "crystal/zones/update_zone.html"
    context_object_name = 'zone'
    success_url = reverse_lazy('horizon:crystal:zones:index')
    page_title = _("Update a Zone")

    def get_context_data(self, **kwargs):
        context = super(UpdateZone, self).get_context_data(**kwargs)
        args = (self.kwargs['zone_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        zone_id = self.kwargs['zone_id']
        try:
            zone = api.get_zone(self.request, zone_id)
            return zone
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve zone details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        zone = self._get_object()
        zone_json = json.loads(zone.text)
        zone_json['zone_id'] = self.kwargs['zone_id']
        return zone_json
