from crystal_dashboard.dashboards.crystal.zones import tables as zone_tables
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from horizon import tables
from horizon import forms
from crystal_dashboard.dashboards.crystal.zones import forms as zone_forms


class IndexView(tables.DataTableView):
    # A very simple class-based view...
    table_class = zone_tables.StoragePolicyTable
    template_name = "crystal/zones/index.html"
    page_title = _("Zones")

    def get_data(self):
        # Add data to the context here...
        return []


class CreateZone(forms.ModalFormView):
    form_class = zone_forms.CreateZone
    form_id = "create_zone_form"

    modal_header = _("Create a Zone")
    submit_label = _("Create a Zone")
    submit_url = reverse_lazy('horizon:crystal:rings:storage_policies:create_storage_policy')
    template_name = "crystal/zones/create_zone.html"
    context_object_name = 'create_zone'
    success_url = reverse_lazy('horizon:crystal:zones:index')
    page_title = _("Create a zone")
