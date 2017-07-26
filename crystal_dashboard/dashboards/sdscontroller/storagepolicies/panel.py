from django.utils.translation import ugettext_lazy as _

import horizon
from crystal_dashboard.dashboards.sdscontroller import dashboard


class Storagepolicies(horizon.Panel):
    name = _("SDS Policies")
    slug = "storagepolicies"


dashboard.SDSController.register(Storagepolicies)
