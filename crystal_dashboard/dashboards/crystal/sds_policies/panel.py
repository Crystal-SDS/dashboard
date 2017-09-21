from django.utils.translation import ugettext_lazy as _
from crystal_dashboard.dashboards.crystal import dashboard
import horizon


class StoragePolicies(horizon.Panel):
    name = _("Policies")
    slug = "sds_policies"


dashboard.CrystalController.register(StoragePolicies)
