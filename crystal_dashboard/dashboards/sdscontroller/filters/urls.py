from django.conf.urls import url, include
from crystal_dashboard.dashboards.sdscontroller.filters import views
from crystal_dashboard.dashboards.sdscontroller.filters.dependencies import urls as dependencies_urls
from crystal_dashboard.dashboards.sdscontroller.filters.filters import urls as filter_urls
from crystal_dashboard.dashboards.sdscontroller.filters.registry_dsl import urls as registry_urls

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'filters/', include(filter_urls, namespace="filters")),
    url(r'dependencies/', include(dependencies_urls, namespace="dependencies")),
    url(r'', include(registry_urls, namespace="registry_dsl")),
]
