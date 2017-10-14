from django.conf.urls import url, include
from crystal_dashboard.dashboards.crystal.policies import views
from crystal_dashboard.dashboards.crystal.policies.policies import urls as policies_urls
from crystal_dashboard.dashboards.crystal.policies.access_control import urls as access_control_urls
from crystal_dashboard.dashboards.crystal.policies.bw_slos import urls as bw_slos_urls
from crystal_dashboard.dashboards.crystal.policies.object_types import urls as object_types_urls

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'policies/', include(policies_urls, namespace='policies')),
    url(r'access_control/', include(access_control_urls, namespace='access_control')),
    url(r'bw_slos/', include(bw_slos_urls, namespace='bw_slos')),
    url(r'object_types/', include(object_types_urls, namespace="object_types"))
]
