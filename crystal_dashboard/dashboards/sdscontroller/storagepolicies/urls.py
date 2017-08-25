from django.conf.urls import url, include
from crystal_dashboard.dashboards.sdscontroller.storagepolicies import views
from crystal_dashboard.dashboards.sdscontroller.storagepolicies.policies import urls as policies_urls

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'policies/', include(policies_urls, namespace='policies')),
    url(r'^\?tab=policies_group_tab__policy_tab$', views.IndexView.as_view(), name='policy_tab')
]
