from django.utils.translation import ugettext_lazy as _
from crystal_dashboard.dashboards.crystal import dashboard
import horizon


class Policies(horizon.Panel):
    name = _("Policies")
    slug = "policies"


dashboard.CrystalController.register(Policies)
