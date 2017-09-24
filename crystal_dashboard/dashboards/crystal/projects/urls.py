from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.projects import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<project_id>[^/]+)/detail/$',
        views.DetailProjectView.as_view(), name='detail'),
]
