from django.conf.urls import url
from crystal_dashboard.dashboards.sdscontroller.projects import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create$', views.CreateProjectView.as_view(), name='create'),
    url(r'^(?P<tenant_id>[^/]+)/update/$',
        views.UpdateProjectView.as_view(), name='update'),
    url(r'^(?P<project_id>[^/]+)/usage/$',
        views.ProjectUsageView.as_view(), name='usage'),
    url(r'^(?P<project_id>[^/]+)/detail/$',
        views.DetailProjectView.as_view(), name='detail'),
]
