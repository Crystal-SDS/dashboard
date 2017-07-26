from django.conf.urls import patterns
from django.conf.urls import url

from crystal_dashboard.dashboards.sdscontroller.bandwidth_differentiation.controllers import views

VIEWS_MOD = "crystal_dashboard.dashboards.sdscontroller.bandwidth_differentiation.controllers.views"

urlpatterns = patterns(
    VIEWS_MOD,
    url(r'^create_get_controller/$', views.CreateGETView.as_view(), name='create_get_controller'),
    url(r'^create_put_controller/$', views.CreatePUTView.as_view(), name='create_put_controller'),
    url(r'^create_replication_controller/$', views.CreateReplicationView.as_view(), name='create_replication_controller'),
)
