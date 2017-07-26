# The name of the dashboard to be added to HORIZON['dashboards']. Required.
DASHBOARD = 'sdscontroller'

# If set to True, this dashboard will not be added to the settings.
DISABLED = False

# A list of applications to be added to INSTALLED_APPS.
ADD_INSTALLED_APPS = [
    'crystal_dashboard.dashboards.sdscontroller',
]
