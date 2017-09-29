from django.utils.translation import ugettext_lazy as _
from crystal_dashboard.dashboards.crystal import dashboard
import horizon


class BandwidthDifferentiation(horizon.Panel):
    name = _("Bandwidth Differentiation")
    slug = 'bandwidth_differentiation'


dashboard.CrystalController.register(BandwidthDifferentiation)
