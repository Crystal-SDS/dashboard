from django.utils.translation import ugettext_lazy as _
from horizon import tabs

from crystal_dashboard.dashboards.crystal.controllers import tabs as controller_tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = controller_tabs.ControllerTabs
    template_name = 'crystal/controllers/index.html'
    page_title = _("Controllers")

    def get_data(self, request, context, *args, **kwargs):
        return context
