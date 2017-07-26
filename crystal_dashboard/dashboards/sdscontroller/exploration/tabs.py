from django.utils.translation import ugettext_lazy as _

from horizon import tabs


class ExplorationTab(tabs.TableTab):
    name = _("Exploration")
    slug = "exploration_plots"
    template_name = "horizon/sdscontroller/exploration/system/_exploration.html"


#class SwiftTab(tabs.TableTab):
#    name = _("Swift")
#    slug = "swift_plots"
#    template_name = "horizon/sdscontroller/storagemonitoring/system/_swift_plots.html"


# class PlotEditor(tabs.TableTab):
#     name = _("Grafana Plot Editor")
#     slug = "grafana_plot_editor"
#     template_name = "horizon/dashboards/sdscontroller/system/_grafana_admin.html"

from openstack_dashboard.dashboards.sdscontroller.administration.registry_dsl import tables as registry_tables


#class PlotEditor(tabs.TableTab):
#    table_classes = (registry_tables.InstancesTable,)
#    name = _("Tenant List")
#    slug = "tenant_list_table"
#    template_name = ("horizon/common/_detail_table.html")
#
#    def get_instances_data(self):
#        return []


class MypanelTabs(tabs.TabGroup):
    slug = "monitoring_tabs"
    tabs = (ExplorationTab)
    sticky = True


# from django.utils.translation import ugettext_lazy as _
#
# from horizon import exceptions
# from horizon import tabs
# import json
#
# from openstack_dashboard.dashboards.sdscontroller.administration.registry_dsl import tables as registry_tables
# from openstack_dashboard.dashboards.sdscontroller.administration.filters import tables as filter_tables
# from openstack_dashboard.dashboards.sdscontroller.administration.filters import models as filters_models
# from openstack_dashboard.dashboards.sdscontroller.administration.registry_dsl import models as registry_models
#
# from openstack_dashboard.dashboards.sdscontroller import api_sds_controller as api
#
#
# class RegistryTab(tabs.TableTab):
#     table_classes = (registry_tables.DslFilterTable,)
#     name = _("Registry DSL")
#     slug = "registry_table"
#     template_name = ("horizon/common/_detail_table.html")
#
#     def get_dsl_filters_data(self):
#         try:
#             response = api.dsl_get_all_filters()
#             print "CAMAMILLA dsl_filters", response.status_code, "text", response.text
#             if 200 <= response.status_code < 300:
#                 strobj = response.text
#             else:
#                 error_message = 'Unable to get filters.'
#                 raise ValueError(error_message)
#         except Exception as e:
#             strobj = "[]"
#             exceptions.handle(self.request, _(e.message))
#
#         instances = json.loads(strobj)
#         ret = []
#         for inst in instances:
#             ret.append(registry_models.Filter(inst['identifier'], inst['name'], inst['activation_url'], inst['valid_parameters']))
#         return ret
#
#
# class TenantList(tabs.TableTab):
#     table_classes = (registry_tables.InstancesTable,)
#     name = _("Tenant List")
#     slug = "tenant_list_table"
#     template_name = ("horizon/common/_detail_table.html")
#
#     def get_instances_data(self):
#             return []
#
#
# class Filters(tabs.TableTab):
#     table_classes = (filter_tables.FilterTable,)
#     name = _("Filters")
#     slug = "filters_table"
#     template_name = ("horizon/common/_detail_table.html")
#
#     def get_filters_data(self):
#         try:
#             response = api.fil_list_filters()
#             if 200 <= response.status_code < 300:
#                 strobj = response.text
#             else:
#                 error_message = 'Unable to get instances.'
#                 raise ValueError(error_message)
#         except Exception as e:
#             strobj = "[]"
#             exceptions.handle(self.request, _(e.message))
#
#         instances = json.loads(strobj)
#         ret = []
#         for inst in instances:
#             ret.append(filters_models.Filter(inst["id"], inst['name'], inst['language'], inst['dependencies'], inst['interface_version'], inst['object_metadata'], inst['main']))
#         return ret
#
#
# class BW(tabs.TableTab):
#     table_classes = (registry_tables.InstancesTable,)
#     name = _("BW Differentiation")
#     slug = "bw__table"
#     template_name = ("horizon/common/_detail_table.html")
#
#     def get_instances_data(self):
#             return []
#
#
# class MypanelTabs(tabs.TabGroup):
#     slug = "mypanel_tabs"
#     tabs = (RegistryTab, Filters, BW, TenantList)
#     sticky = True
#
