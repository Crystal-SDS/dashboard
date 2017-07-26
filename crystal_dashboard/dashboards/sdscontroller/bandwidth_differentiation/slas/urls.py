from django.conf.urls import patterns
from django.conf.urls import url

from crystal_dashboard.dashboards.sdscontroller.bandwidth_differentiation.slas import views

VIEWS_MOD = "crystal_dashboard.dashboards.sdscontroller.bandwidth_differentiation.slas.views"

urlpatterns = patterns(
    VIEWS_MOD,
    url(r'^create_sla/$', views.CreateView.as_view(), name='create_sla'),
    url(r'^update_sla/(?P<sla_id>[^/]+)/$', views.UpdateView.as_view(), name='update_sla'),
)
