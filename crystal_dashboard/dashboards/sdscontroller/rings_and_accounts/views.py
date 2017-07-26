# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from horizon import tabs
from openstack_dashboard.dashboards.sdscontroller.rings_and_accounts \
    import tabs as mydashboard_tabs

class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = mydashboard_tabs.MypanelTabs
    template_name = 'sdscontroller/rings_and_accounts/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context
