from crystal_dashboard.dashboards.crystal.rings.storage_policies import tables as storagepolicies_tables
from crystal_dashboard.dashboards.crystal.rings.storage_policies import models as storage_policies_models
from crystal_dashboard.api import swift as api
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import tabs
import json


class StoragePolicies(tabs.TableTab):
    table_classes = (storagepolicies_tables.StoragePolicyTable,)
    name = _("Storage Policies")
    slug = "storagepolicies_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_storagepolicies_data(self):
        try:
            response = api.swift_list_storage_policies(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get storage nodes.'
                raise ValueError(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            parameters = ', '.join([key.replace('_', ' ').title()+':'+inst[key] for key in inst.keys() if key not in ['id', 'name', 'policy_type', 'default', 'devices', 'deprecated', 'deployed']])
            ret.append(storage_policies_models.StoragePolicy(inst['id'], inst['name'], inst['policy_type'], inst['default'], parameters, inst['deprecated'], inst['deployed'], len(inst['devices'])))
        return ret


class RingsTabs(tabs.TabGroup):
    slug = "rings_tabs"
    tabs = (StoragePolicies,)
    sticky = True
