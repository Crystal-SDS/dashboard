from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.controllers.instances import views

urlpatterns = [
    url(r'^create_instance/$', views.CreateInstanceView.as_view(), name='create_instance'),
    url(r'^update_instance/(?P<id>[^/]+)/$', views.UpdateInstanceView.as_view(), name='update_instance'),

]
