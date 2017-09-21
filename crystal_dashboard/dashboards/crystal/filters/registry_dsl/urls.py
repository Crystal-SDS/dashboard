from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.filters.registry_dsl import views

urlpatterns = [
    url(r'^create_filter', views.CreateFilterView.as_view(), name='create_filter'),
    url(r'^update_filter/(?P<name>[^/]+)/$', views.UpdateFilterView.as_view(), name='update_filter')
]
