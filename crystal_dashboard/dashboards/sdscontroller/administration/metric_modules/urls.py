from django.conf.urls import patterns
from django.conf.urls import url

from crystal_dashboard.dashboards.sdscontroller.administration.metric_modules import views

VIEWS_MOD = 'crystal_dashboard.dashboards.sdscontroller.administration.metric_modules.views'

urlpatterns = patterns(
    VIEWS_MOD,
    url(r'^upload_metric_module/$', views.UploadView.as_view(), name='upload_metric_module'),
    url(r'^download_metric_module/(?P<metric_module_id>[^/]+)/$', views.download_metric_module, name='download_metric_module'),
    url(r'^update_metric_module/(?P<metric_module_id>[^/]+)/$', views.UpdateView.as_view(), name='update_metric_module'),
)
