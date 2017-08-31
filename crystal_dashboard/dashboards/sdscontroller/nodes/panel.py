from django.utils.translation import ugettext_lazy as _
from crystal_dashboard.dashboards.sdscontroller import dashboard
import horizon


class Nodes(horizon.Panel):
    name = _("Nodes")
    slug = "nodes"


dashboard.CrystalController.register(Nodes)
