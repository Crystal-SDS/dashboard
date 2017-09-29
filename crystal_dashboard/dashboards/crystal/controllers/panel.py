from django.utils.translation import ugettext_lazy as _
from crystal_dashboard.dashboards.crystal import dashboard
import horizon


class Controllers(horizon.Panel):
    name = _("Controllers")
    slug = 'controllers'


dashboard.CrystalController.register(Controllers)
