from horizon import tabs

from crystal_dashboard.dashboards.sdscontroller.administration import tabs as administration_tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = administration_tabs.MyPanelTabs
    template_name = 'sdscontroller/administration/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context
