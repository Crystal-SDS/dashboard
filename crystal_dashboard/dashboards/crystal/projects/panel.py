from django.utils.translation import ugettext_lazy as _
from crystal_dashboard.dashboards.crystal import dashboard
import horizon


class Tenants(horizon.Panel):
    name = _("Projects")
    slug = 'projects'
    policy_rules = (("crystal", "crystal:list_projects"),
                    ("crystal", "crystal:list_user_projects"))

dashboard.CrystalController.register(Tenants)
