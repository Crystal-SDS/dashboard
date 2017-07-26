from horizon import tabs

from openstack_dashboard.dashboards.sdscontroller.bandwidth_differentiation import tabs as mydashboard_tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = mydashboard_tabs.MypanelTabs
    template_name = 'sdscontroller/bandwidth_differentiation/index.html'

    def get_data(self, request, context, *args, **kwargs):
        return context
