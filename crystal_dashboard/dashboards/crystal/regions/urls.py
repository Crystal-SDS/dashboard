from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.regions.views import IndexView
from crystal_dashboard.dashboards.crystal.regions import views


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^create/', views.CreateRegion.as_view(), name='create'),
    url(r'^update/(?P<region_id>[^/]+)/$', views.UpdateRegion.as_view(), name='update'),
]
