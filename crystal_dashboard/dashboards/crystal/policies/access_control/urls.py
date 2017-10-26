from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.policies.access_control import views

urlpatterns = [
    url(r'^create/$', views.CreateView.as_view(), name='create'),
    url(r'^update/(?P<policy_id>[^/]+)/$', views.UpdateView.as_view(), name='update')
]
