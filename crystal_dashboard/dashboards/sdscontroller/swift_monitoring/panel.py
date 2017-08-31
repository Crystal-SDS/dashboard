from django.utils.translation import ugettext_lazy as _
from crystal_dashboard.dashboards.sdscontroller import dashboard
import horizon


class SwiftMonitoring(horizon.Panel):
    name = _("Swift Cluster")
    slug = "swift_monitoring"


dashboard.CrystalController.register(SwiftMonitoring)
