from django.utils.translation import ugettext_lazy as _
from crystal_dashboard.dashboards.sdscontroller import dashboard
import horizon


class Tenants(horizon.Panel):
    name = _("Projects")
    slug = 'projects'
    policy_rules = (("sdscontroller", "sdscontroller:list_projects"),
                    ("sdscontroller", "sdscontroller:list_user_projects"))

dashboard.CrystalController.register(Tenants)
