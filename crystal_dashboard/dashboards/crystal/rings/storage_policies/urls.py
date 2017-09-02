from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.rings.storage_policies import views

urlpatterns = [
    url(r'^create_storage_policy', views.CreateStoragePolicy.as_view(),
        name='create_storage_policy'),
    url(r'^create_ec_storage_policy', views.CreateECStoragePolicy.as_view(),
        name='create_ec_storage_policy'),
    url(r'^bind_storage_node', views.BindStorageNode.as_view(),
        name='bind_storage_node')
]
