from django.conf.urls import patterns
from django.conf.urls import url

from crystal_dashboard.dashboards.sdscontroller.administration.filters import views

VIEWS_MOD = 'crystal_dashboard.dashboards.sdscontroller.administration.filters.views'

urlpatterns = patterns(
    VIEWS_MOD,
    url(r'^upload_storlet/$', views.UploadStorletView.as_view(), name='upload_storlet'),
    url(r'^upload_native/$', views.UploadNativeView.as_view(), name='upload_native'),
    url(r'^upload_global/$', views.UploadGlobalView.as_view(), name='upload_global'),
    url(r'^download/(?P<filter_id>[^/]+)/$', views.download_filter, name='download'),
    url(r'^update_storlet/(?P<filter_id>[^/]+)/$', views.UpdateStorletView.as_view(), name='update_storlet'),
    url(r'^update_native/(?P<filter_id>[^/]+)/$', views.UpdateNativeView.as_view(), name='update_native'),
    url(r'^update_global/(?P<filter_id>[^/]+)/$', views.UpdateGlobalView.as_view(), name='update_global'),
)
