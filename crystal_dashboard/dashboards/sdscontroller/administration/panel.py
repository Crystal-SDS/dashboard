from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.sdscontroller import dashboard


class Administration(horizon.Panel):
    name = _("Administration")
    slug = "administration"


dashboard.SDSController.register(Administration)
