from django.conf.urls import url, include
from crystal_dashboard.dashboards.sdscontroller.bandwidth_differentiation import views
from crystal_dashboard.dashboards.sdscontroller.bandwidth_differentiation.controllers import urls as controllers_urls
from crystal_dashboard.dashboards.sdscontroller.bandwidth_differentiation.proxy_sorting import urls as proxy_sorting_urls
from crystal_dashboard.dashboards.sdscontroller.bandwidth_differentiation.slas import urls as slas_urls

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'slas/', include(slas_urls, namespace="slas")),
    url(r'controllers/', include(controllers_urls, namespace="controllers")),
    url(r'proxy_sorting/', include(proxy_sorting_urls, namespace="proxy_sorting"))
]
