from django.utils.translation import ugettext_lazy as _
from crystal_dashboard.dashboards.crystal import dashboard
import horizon


class Filters(horizon.Panel):
    name = _("Filters")
    slug = "filters"


dashboard.CrystalController.register(Filters)
