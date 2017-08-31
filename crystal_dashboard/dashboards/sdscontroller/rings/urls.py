from django.conf.urls import url
from django.conf.urls import include
from crystal_dashboard.dashboards.sdscontroller.rings.views import IndexView
from crystal_dashboard.dashboards.sdscontroller.rings.storage_policies import urls as storage_policies


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'', include(storage_policies, namespace="storage_policies")),
]
