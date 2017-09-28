from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.controllers.controllers import views

urlpatterns = [
    url(r'^create_get_controller/$', views.CreateGETView.as_view(), name='create_get_controller'),
]
