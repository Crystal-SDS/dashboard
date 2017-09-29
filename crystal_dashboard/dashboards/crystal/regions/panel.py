from django.utils.translation import ugettext_lazy as _
from crystal_dashboard.dashboards.crystal import dashboard
import horizon


class Regions(horizon.Panel):
    name = _("Regions")
    slug = "regions"


dashboard.CrystalController.register(Regions)
