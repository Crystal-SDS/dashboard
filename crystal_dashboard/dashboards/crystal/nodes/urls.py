from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.nodes import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^update/(?P<server>[^/]+)/(?P<node_id>[^/]+)/$', views.UpdateNodeView.as_view(), name='update')
]
