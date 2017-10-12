from crystal_dashboard.dashboards.crystal.rings import tabs as rings_tabs
from django.utils.translation import ugettext_lazy as _
from horizon import tabs


class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = rings_tabs.RingsTabs
    template_name = 'crystal/rings/index.html'
    page_title = _("Storage Policies")

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context
