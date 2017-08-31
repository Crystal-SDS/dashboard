from django.utils.translation import ugettext_lazy as _
from crystal_dashboard.dashboards.sdscontroller import dashboard
import horizon


class Rings(horizon.Panel):
    name = _("Storage Policies (Rings)")
    slug = "rings"


dashboard.CrystalController.register(Rings)
