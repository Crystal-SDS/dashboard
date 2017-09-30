from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.policies.object_types import views

urlpatterns = [
    url(r'^create', views.CreateObjectTypeView.as_view(), name='create'),
    url(r'^update/(?P<object_type_id>[^/]+)/$', views.UpdateObjectTypeView.as_view(), name='update')
]
