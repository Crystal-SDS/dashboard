from django.utils.translation import ugettext_lazy as _
from crystal_dashboard.dashboards.sdscontroller import dashboard
import horizon


class Kibana(horizon.Panel):
    name = _("Kibana")
    slug = "kibana"


dashboard.CrystalController.register(Kibana)
