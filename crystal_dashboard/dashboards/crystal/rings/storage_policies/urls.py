from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.rings.storage_policies import views

urlpatterns = [
    url(r'^create_storage_policy', views.CreateStoragePolicy.as_view(),
        name='create_storage_policy'),
    url(r'^update_storage_policy/(?P<id>[^/]+)/$', views.UpdateStoragePolicy.as_view(), name='update_storage_policy'),
    url(r'^create_ec_storage_policy', views.CreateECStoragePolicy.as_view(),
        name='create_ec_storage_policy'),
    url(r'^load_swift_policies', views.LoadSwiftPolicies.as_view(),
        name='load_swift_policies'),
    url(r'^(?P<policy_id>[^/]+)/devices/$', views.ManageDisksView.as_view(),
        name='devices'),
    url(r'^(?P<policy_id>[^/]+)/add_devices/$', views.AddDisksView.as_view(),
        name='add_devices'),
]
