from django.conf.urls import url
from crystal_dashboard.dashboards.sdscontroller.exploration.views \
    import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index')
]
