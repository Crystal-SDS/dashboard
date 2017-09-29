from django.conf.urls import url, include
from crystal_dashboard.dashboards.crystal.bandwidth_differentiation import views
from crystal_dashboard.dashboards.crystal.bandwidth_differentiation.slas import urls as slas_urls

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'slas/', include(slas_urls, namespace="slas")),
]
