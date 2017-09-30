from django.conf.urls import url
from crystal_dashboard.dashboards.crystal.policies.policies import views

urlpatterns = [
    url(r'^create_static_policy/$', views.CreateStaticPolicyView.as_view(), name='create_static_policy'),
    url(r'^create_dsl_policy/$', views.CreateDSLPolicyView.as_view(), name='create_dsl_policy'),
    url(r'^update_static_policy/(?P<policy_id>[^/]+)/$', views.UpdateStaticPolicyView.as_view(), name='update_static_policy'),
    url(r'^get_container_by_project/$', views.get_container_by_project, name='get_container_by_project'),
]
