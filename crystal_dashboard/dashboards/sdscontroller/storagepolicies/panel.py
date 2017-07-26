from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.sdscontroller import dashboard


class Storagepolicies(horizon.Panel):
    name = _("SDS Policies")
    slug = "storagepolicies"


dashboard.SDSController.register(Storagepolicies)
