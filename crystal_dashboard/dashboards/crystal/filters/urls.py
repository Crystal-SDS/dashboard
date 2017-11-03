from django.conf.urls import url, include
from crystal_dashboard.dashboards.crystal.filters import views
from crystal_dashboard.dashboards.crystal.filters.dependencies import urls as dependencies_urls
from crystal_dashboard.dashboards.crystal.filters.filters import urls as filter_urls

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'filters/', include(filter_urls, namespace="filters")),
    url(r'dependencies/', include(dependencies_urls, namespace="dependencies")),
]
