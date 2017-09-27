from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.filters.filters import views

urlpatterns = [
    url(r'^upload_storlet/$', views.UploadStorletView.as_view(), name='upload_storlet'),
    url(r'^upload_native/$', views.UploadNativeView.as_view(), name='upload_native'),
    url(r'^download/(?P<filter_id>[^/]+)/$', views.download_filter, name='download'),
    url(r'^update_storlet/(?P<filter_id>[^/]+)/$', views.UpdateStorletView.as_view(), name='update_storlet'),
    url(r'^update_native/(?P<filter_id>[^/]+)/$', views.UpdateNativeView.as_view(), name='update_native'),
]
