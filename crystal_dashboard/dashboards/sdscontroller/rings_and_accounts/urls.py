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

from django.conf.urls import patterns
from django.conf.urls import url
from django.conf.urls import include

from openstack_dashboard.dashboards.sdscontroller.rings_and_accounts.views \
    import IndexView
from openstack_dashboard.dashboards.sdscontroller.rings_and_accounts.storage_policies import urls as storage_policies


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'', include(storage_policies, namespace="storage_policies")),
)
