from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.sdscontroller import dashboard


class BandwidthDifferentiation(horizon.Panel):
    name = _("Bandwidth Differentiation")
    slug = 'bandwidth_differentiation'


dashboard.SDSController.register(BandwidthDifferentiation)
