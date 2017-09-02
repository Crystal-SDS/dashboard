from django.utils.translation import ugettext_lazy as _
from crystal_dashboard.dashboards.crystal import dashboard
import horizon


class Nodes(horizon.Panel):
    name = _("Nodes")
    slug = "nodes"


dashboard.CrystalController.register(Nodes)
