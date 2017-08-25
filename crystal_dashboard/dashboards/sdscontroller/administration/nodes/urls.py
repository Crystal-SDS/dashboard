from django.conf.urls import url
from crystal_dashboard.dashboards.sdscontroller.administration.nodes import views

urlpatterns = [
    url(r'^update/(?P<server>[^/]+)/(?P<node_id>[^/]+)/$', views.UpdateNodeView.as_view(), name='update')
]
