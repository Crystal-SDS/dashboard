from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.kibana.views \
    import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index')
]
