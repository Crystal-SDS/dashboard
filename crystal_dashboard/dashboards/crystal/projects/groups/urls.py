from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.projects.groups import views

urlpatterns = [
    url(r'^create/$', views.CreateGroupView.as_view(), name='create'),
    url(r'^update/(?P<id>[^/]+)/$', views.UpdateGroupView.as_view(), name='update'),
]
