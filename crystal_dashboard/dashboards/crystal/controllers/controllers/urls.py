from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.controllers.controllers import views

urlpatterns = [
    url(r'^create_controller/$', views.CreateControllerView.as_view(), name='create_controller'),
    url(r'^update_controller/(?P<id>[^/]+)/$', views.UpdateControllerView.as_view(), name='update_controller'),
    url(r'^launch_instance/(?P<id>[^/]+)/$', views.LaunchInstanceView.as_view(), name='launch_instance'),


]
