from horizon import tabs

from crystal_dashboard.dashboards.crystal.analytics_jobs import tabs as analytics_jobs_tabs

class IndexView(tabs.TabbedTableView):
    tab_group_class = analytics_jobs_tabs.MyPanelTabs
    template_name = 'sdscontroller/analytics_jobs/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context