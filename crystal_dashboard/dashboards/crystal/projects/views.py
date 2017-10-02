from crystal_dashboard.dashboards.crystal.projects import tabs as projects_tabs
from django.utils.translation import ugettext_lazy as _
from horizon import tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = projects_tabs.ProjectsTabs
    template_name = 'crystal/projects/index.html'
    page_title = _("Projects")

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context
