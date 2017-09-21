from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.bandwidth_differentiation.controllers import views

urlpatterns = [
    url(r'^create_get_controller/$', views.CreateGETView.as_view(), name='create_get_controller'),
    url(r'^create_put_controller/$', views.CreatePUTView.as_view(), name='create_put_controller'),
    url(r'^create_replication_controller/$', views.CreateReplicationView.as_view(), name='create_replication_controller')
]
