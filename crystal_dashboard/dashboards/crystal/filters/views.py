from crystal_dashboard.dashboards.crystal.filters import tabs as filters_tabs
from django.utils.translation import ugettext_lazy as _
from horizon import tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = filters_tabs.FiltersTabs
    template_name = 'crystal/filters/index.html'
    page_title = _("Filters")

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context
