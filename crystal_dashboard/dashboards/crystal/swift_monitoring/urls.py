from django.conf.urls import url
import crystal_dashboard.dashboards.crystal.swift_monitoring.views as views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^system$', views.SystemView.as_view(), name='system'),
    url(r'^swift_container', views.SwiftContainerView.as_view(), name='swift_container')
]
