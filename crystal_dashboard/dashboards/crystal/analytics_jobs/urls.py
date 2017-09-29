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

from django.conf.urls import include
from django.conf.urls import url

import crystal_dashboard.dashboards.crystal.analytics_jobs.views as views

from crystal_dashboard.dashboards.crystal.analytics_jobs.analyzers import urls as analyzers_urls
from crystal_dashboard.dashboards.crystal.analytics_jobs.jobs import urls as jobs_urls


urlpatterns = [
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'analyzers/', include(analyzers_urls, namespace="analyzers")),
    url(r'jobs/', include(jobs_urls, namespace="jobs")),

]