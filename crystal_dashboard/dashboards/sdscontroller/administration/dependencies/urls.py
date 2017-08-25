from django.conf.urls import url
from crystal_dashboard.dashboards.sdscontroller.administration.dependencies import views

urlpatterns = [
    url(r'^upload/$', views.UploadView.as_view(), name='upload'),
    url(r'^update/(?P<dependency_id>[^/]+)/$', views.UpdateView.as_view(), name='update')
]
