from django.conf.urls import url, include
from crystal_dashboard.dashboards.crystal.projects import views
from crystal_dashboard.dashboards.crystal.projects.groups import urls as groups_urls

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'groups/', include(groups_urls, namespace="groups")),
]
