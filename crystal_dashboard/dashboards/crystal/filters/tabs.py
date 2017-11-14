from crystal_dashboard.api import filters as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from crystal_dashboard.dashboards.crystal.filters.dependencies import models as dependency_models
from crystal_dashboard.dashboards.crystal.filters.dependencies import tables as dependency_tables
from crystal_dashboard.dashboards.crystal.filters.filters import models as filters_models
from crystal_dashboard.dashboards.crystal.filters.filters import tables as filter_tables
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import tabs
import json


class NativeFilters(tabs.TableTab):
    table_classes = (filter_tables.NativeFilterTable,)
    name = _("Native Filters")
    slug = "native_filters_table"
    template_name = "crystal/filters/filters/_detail.html"
    response = None
    preload = False

    def get_native_filters_data(self):
        try:
            if not self.response:
                self.response = api.list_filters(self.request)
            if 200 <= self.response.status_code < 300:
                strobj = self.response.text
            else:
                error_message = 'Unable to get filters.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            if inst['filter_type'] == 'native':
                if inst['execution_server'] == 'proxy':
                    inst['execution_server'] = 'Proxy Node'
                elif inst['execution_server'] == 'object':
                    inst['execution_server'] = 'Storage Node'
                if inst['reverse'] == 'proxy':
                    inst['reverse'] = 'Proxy Node'
                elif inst['reverse'] == 'object':
                    inst['reverse'] = 'Storage Node'
                ret.append(filters_models.Filter(inst['dsl_name'], inst['filter_name'], inst['dsl_name'], inst['filter_type'],
                                                 inst['language'], inst['dependencies'], None, inst['main'],
                                                 inst['execution_server'], inst['reverse'], inst['put'], inst['get'], inst['post'], 
                                                 inst['head'], inst['delete'], inst['valid_parameters']))
        return ret


class StorletFilters(tabs.TableTab):
    table_classes = (filter_tables.StorletFilterTable,)
    name = _("Storlet Filters")
    slug = "storlet_filters_table"
    template_name = "crystal/filters/filters/_detail.html"
    response = None
    preload = False

    def get_storlet_filters_data(self):
        try:
            if not self.response:
                self.response = api.list_filters(self.request)
            if 200 <= self.response.status_code < 300:
                strobj = self.response.text
            else:
                error_message = 'Unable to get filters.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            if inst['filter_type'] == 'storlet':
                if inst['execution_server'] == 'proxy':
                    inst['execution_server'] = 'Proxy Node'
                elif inst['execution_server'] == 'object':
                    inst['execution_server'] = 'Storage Node'
                if inst['reverse'] == 'proxy':
                    inst['reverse'] = 'Proxy Node'
                elif inst['reverse'] == 'object':
                    inst['reverse'] = 'Storage Node'
                ret.append(filters_models.Filter(inst['dsl_name'], inst['filter_name'], inst['dsl_name'], inst['filter_type'],
                                                 inst['language'], inst['dependencies'], inst['interface_version'], inst['main'],
                                                 inst['execution_server'], inst['reverse'], inst['put'], inst['get'], False, 
                                                 False, False, inst['valid_parameters']))
        return ret


class Dependencies(tabs.TableTab):
    table_classes = (dependency_tables.DependenciesTable,)
    name = _("Dependencies")
    slug = "dependencies_table"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_dependencies_data(self):
        try:
            response = api.list_dependencies(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get dependencies.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        dependencies = json.loads(strobj)
        ret = []
        for dep in dependencies:
            ret.append(dependency_models.Dependency(dep['id'], dep['name'], dep['version'], dep['permissions']))
        return ret


class FiltersTabs(tabs.TabGroup):
    slug = "filters_tabs"
    tabs = (NativeFilters, StorletFilters,)
    sticky = True
