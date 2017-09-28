import json

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
from crystal_dashboard.api import controllers as api
from crystal_dashboard.dashboards.crystal import common
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from crystal_dashboard.dashboards.crystal.controllers.controllers import models as controllers_models
from crystal_dashboard.dashboards.crystal.controllers.controllers import tables as controllers_tables


class ControllersTab(tabs.TableTab):
    table_classes = (controllers_tables.ControllersGETTable,)
    name = _("Controllers")
    slug = "controllers_table"
    # template_name = "horizon/common/_detail_table.html"
    template_name = "crystal/controllers/controllers/_detail.html"
    preload = False
    response = None

    def get_get_controllers_data(self):
        try:
            if not self.response:
                self.response = api.dsl_get_all_global_controllers(self.request)
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
            if inst['dsl_filter'] == 'bandwidth' and inst['type'] == 'get':
                ret.append(controllers_models.Controller(inst['id'], inst['controller_name'], inst['class_name'], inst['enabled']))
        return ret

    def get_put_controllers_data(self):
        try:
            if not self.response:
                self.response = api.dsl_get_all_global_controllers(self.request)
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
            if inst['dsl_filter'] == 'bandwidth' and inst['type'] == 'put':
                ret.append(controllers_models.Controller(inst['id'], inst['controller_name'], inst['class_name'], inst['enabled']))
        return ret

    def get_replication_controllers_data(self):
        try:
            if not self.response:
                self.response = api.dsl_get_all_global_controllers(self.request)
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
            if inst['dsl_filter'] == 'bandwidth' and inst['type'] == 'ssync':
                ret.append(controllers_models.Controller(inst['id'], inst['controller_name'], inst['class_name'], inst['enabled']))
        return ret


class BwDiffTabs(tabs.TabGroup):
    slug = "controllers_tabs"
    # tabs = (SLAsTab, ProxySortingTab,)
    tabs = (ControllersTab,)
    sticky = True
