from django.utils.translation import ugettext_lazy as _
from crystal_dashboard.dashboards.crystal.policies import tabs as policies_tabs
from horizon import tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = policies_tabs.PoliciesGroupTabs
    template_name = 'crystal/policies/index.html'
    page_title = _("Policies")
