from django.conf.urls import url, include
from crystal_dashboard.dashboards.sdscontroller.sds_policies import views
from crystal_dashboard.dashboards.sdscontroller.sds_policies.policies import urls as policies_urls
from crystal_dashboard.dashboards.sdscontroller.sds_policies.object_types import urls as object_types_urls

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'policies/', include(policies_urls, namespace='policies')),
    url(r'object_types/', include(object_types_urls, namespace="object_types"))
]
