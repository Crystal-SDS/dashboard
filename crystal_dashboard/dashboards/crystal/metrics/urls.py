from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.metrics import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^upload_metric_module/$', views.UploadView.as_view(), name='upload_metric_module'),
    url(r'^download_metric_module/(?P<metric_module_id>[^/]+)/$', views.download_metric_module, name='download_metric_module'),
    url(r'^update_metric_module/(?P<metric_module_id>[^/]+)/$', views.UpdateView.as_view(), name='update_metric_module')
]
