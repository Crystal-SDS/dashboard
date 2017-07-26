from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.sdscontroller.administration.dependencies import views

VIEWS_MOD = 'openstack_dashboard.dashboards.sdscontroller.administration.dependencies.views'

urlpatterns = patterns(
    VIEWS_MOD,
    url(r'^upload/$', views.UploadView.as_view(), name='upload'),
    url(r'^update/(?P<dependency_id>[^/]+)/$', views.UpdateView.as_view(), name='update'),
)
