from django.utils.translation import ugettext_lazy as _
from crystal_dashboard.dashboards.sdscontroller import dashboard
import horizon


class Filters(horizon.Panel):
    name = _("Filters")
    slug = "filters"


dashboard.CrystalController.register(Filters)
