from django.conf.urls import url
from crystal_dashboard.dashboards.sdscontroller.bandwidth_differentiation.slas import views

urlpatterns = [
    url(r'^create_sla/$', views.CreateView.as_view(), name='create_sla'),
    url(r'^update_sla/(?P<sla_id>[^/]+)/$', views.UpdateView.as_view(), name='update_sla')
]
