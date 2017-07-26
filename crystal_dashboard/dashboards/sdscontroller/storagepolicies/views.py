from django.utils.translation import ugettext_lazy as _

from horizon import tabs
from crystal_dashboard.dashboards.sdscontroller.storagepolicies import tabs as policies_tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = policies_tabs.PoliciesGroupTabs
    template_name = 'sdscontroller/storagepolicies/index.html'
    page_title = _("Policies")
