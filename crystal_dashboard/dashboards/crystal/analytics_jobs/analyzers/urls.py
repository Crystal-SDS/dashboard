from django.conf.urls import patterns
from django.conf.urls import url

from crystal_dashboard.dashboards.crystal.analytics_jobs.analyzers import views

VIEWS_MOD = 'crystal_dashboard.dashboards.crystal.analytics_jobs.analyzers.views'

urlpatterns = patterns(
    VIEWS_MOD,
    url(r'^create_analyzer/$', views.CreateAnalyzerView.as_view(), name='create_analyzer'),
    url(r'^download_analyzer/(?P<analyzer_id>[^/]+)/$', views.download_analyzer, name='download_analyzer'),
)
