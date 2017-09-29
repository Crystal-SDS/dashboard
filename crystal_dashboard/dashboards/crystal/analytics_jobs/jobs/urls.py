from django.conf.urls import patterns
from django.conf.urls import url

from crystal_dashboard.dashboards.crystal.analytics_jobs.jobs import views

urlpatterns = patterns(
    url(r'^submit_job/$', views.SubmitJobView.as_view(), name='submit_job'),
)
