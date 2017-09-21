from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.bandwidth_differentiation.proxy_sorting import views

urlpatterns = [
    url(r'^upload/$', views.UploadView.as_view(), name='upload'),
    url(r'^update/(?P<proxy_sorting_id>[^/]+)/$', views.UpdateView.as_view(), name='update')
]
