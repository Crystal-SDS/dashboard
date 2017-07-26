from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

from crystal_dashboard.dashboards.sdscontroller.administration import views
from crystal_dashboard.dashboards.sdscontroller.administration.dependencies import urls as dependencies_urls
from crystal_dashboard.dashboards.sdscontroller.administration.filters import urls as filter_urls
from crystal_dashboard.dashboards.sdscontroller.administration.metric_modules import urls as metric_modules_urls
from crystal_dashboard.dashboards.sdscontroller.administration.nodes import urls as nodes_urls
from crystal_dashboard.dashboards.sdscontroller.administration.object_types import urls as object_types_urls
from crystal_dashboard.dashboards.sdscontroller.administration.registry_dsl import urls as registry_urls

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       url(r'dependencies/', include(dependencies_urls, namespace="dependencies")),
                       url(r'filters/', include(filter_urls, namespace="filters")),
                       url(r'', include(registry_urls, namespace="registry_dsl")),
                       url(r'object_types/', include(object_types_urls, namespace="object_types")),
                       url(r'metric_modules/', include(metric_modules_urls, namespace="metric_modules")),
                       url(r'nodes/', include(nodes_urls, namespace="nodes")),
                       )
