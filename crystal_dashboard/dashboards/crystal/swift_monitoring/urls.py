from django.conf.urls import url
import crystal_dashboard.dashboards.crystal.swift_monitoring.views as views

urlpatterns = [
    url(r'^$', views.CrystalDashboard.as_view(), name='index'),
]
