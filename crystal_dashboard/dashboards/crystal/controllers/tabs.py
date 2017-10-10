from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import tabs
import json
from crystal_dashboard.api import controllers as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from crystal_dashboard.dashboards.crystal.controllers.controllers import models as controllers_models
from crystal_dashboard.dashboards.crystal.controllers.controllers import tables as controllers_tables
from crystal_dashboard.dashboards.crystal.controllers.instances import tables as instances_tables
from crystal_dashboard.dashboards.crystal.controllers.instances import models as instances_models


class ControllersTab(tabs.TableTab):
    table_classes = (controllers_tables.ControllersTable,)
    name = _("Controllers")
    slug = "controllers_table"
    template_name = "crystal/controllers/controllers/_detail.html"
    preload = False
    response = None

    def get_controllers_data(self):
        try:
            if not self.response:
                self.response = api.get_all_controllers(self.request)
            if 200 <= self.response.status_code < 300:
                strobj = self.response.text
            else:
                error_message = 'Unable to get instances.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            ctrl = controllers_models.Controller(inst['id'], inst['controller_name'], inst['description'],
                                                 inst['class_name'], inst['instances'], inst['valid_parameters'])
            ret.append(ctrl)
        return ret


class InstancesTab(tabs.TableTab):
    table_classes = (instances_tables.InstancesTable,)
    name = _("Instances")
    slug = "instances_table"
    template_name = "crystal/controllers/instances/_detail.html"
    preload = False
    response = None

    def get_instances_data(self):
        instances = json.loads(api.get_all_instances(self.request).text)
        return [instances_models.Instance(instance['id'], instance['controller'], instance['parameters'], 
                                          instance['description'], instance['status']) for instance in instances] 


class ControllerTabs(tabs.TabGroup):
    slug = "controllers_tabs"
    tabs = (ControllersTab, InstancesTab,)
    sticky = True
