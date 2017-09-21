from django.utils.translation import ugettext_lazy as _
from crystal_dashboard.dashboards.crystal import dashboard
import horizon


class WorkloadMetrics(horizon.Panel):
    name = _("Workload Metrics")
    slug = "workload_metrics"


dashboard.CrystalController.register(WorkloadMetrics)
