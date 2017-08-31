from django.utils.translation import ugettext_lazy as _
from horizon import tabs

from crystal_dashboard.dashboards.sdscontroller.bandwidth_differentiation import tabs as BwDIff_tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = BwDIff_tabs.BwDiffTabs
    template_name = 'sdscontroller/bandwidth_differentiation/index.html'
    page_title = _("Bandwidth Differentiation")

    def get_data(self, request, context, *args, **kwargs):
        return context
