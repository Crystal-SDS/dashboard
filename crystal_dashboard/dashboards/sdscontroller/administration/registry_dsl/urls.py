from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.sdscontroller.administration.registry_dsl import views

VIEWS_MOD = 'openstack_dashboard.dashboards.sdscontroller.administration.registry_dsl.views'

urlpatterns = patterns(
    VIEWS_MOD,
    url(r'^create_filter', views.CreateFilterView.as_view(), name='create_filter'),
    url(r'^update_filter/(?P<name>[^/]+)/$', views.UpdateFilterView.as_view(), name='update_filter'),
)
