from django.conf.urls import url, include
from crystal_dashboard.dashboards.crystal.controllers import views
from crystal_dashboard.dashboards.crystal.controllers.controllers import urls as controllers_urls
from crystal_dashboard.dashboards.crystal.controllers.instances import urls as instances_urls

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'controllers/', include(controllers_urls, namespace="controllers")),
    url(r'instances/', include(instances_urls, namespace="instances")),
]
