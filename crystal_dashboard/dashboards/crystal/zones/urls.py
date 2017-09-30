from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.zones.views import IndexView
from crystal_dashboard.dashboards.crystal.zones import views


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^create/', views.CreateZone.as_view(), name='create'),
    url(r'^update/(?P<zone_id>[^/]+)/$', views.UpdateZone.as_view(), name='update'),
]
