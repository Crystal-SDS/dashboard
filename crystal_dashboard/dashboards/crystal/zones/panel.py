from django.utils.translation import ugettext_lazy as _
from crystal_dashboard.dashboards.crystal import dashboard
import horizon


class Zones(horizon.Panel):
    name = _("Zones")
    slug = "zones"


dashboard.CrystalController.register(Zones)
