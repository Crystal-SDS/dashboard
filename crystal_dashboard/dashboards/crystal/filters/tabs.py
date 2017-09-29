from crystal_dashboard.api import filters as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from crystal_dashboard.dashboards.crystal.filters.dependencies import models as dependency_models
from crystal_dashboard.dashboards.crystal.filters.dependencies import tables as dependency_tables
from crystal_dashboard.dashboards.crystal.filters.filters import models as filters_models
from crystal_dashboard.dashboards.crystal.filters.filters import tables as filter_tables
from crystal_dashboard.dashboards.crystal.filters.groups import models as group_models
from crystal_dashboard.dashboards.crystal.filters.groups import tables as group_tables
from crystal_dashboard.dashboards.crystal.filters.registry_dsl import models as registry_models
from crystal_dashboard.dashboards.crystal.filters.registry_dsl import tables as registry_tables
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import tabs
import json


class RegistryTab(tabs.TableTab):
    table_classes = (registry_tables.DslFilterTable,)
    name = _("Registry DSL")
    slug = "registry_table"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_dsl_filters_data(self):
        try:
            response = api.dsl_get_all_filters(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get filters.'
                raise ValueError(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, e.message)

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            response = api.fil_get_filter_metadata(self.request, inst['identifier'])
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get filters.'
                raise ValueError(error_message)
            _filter = json.loads(strobj)
            ret.append(registry_models.Filter(inst['identifier'], inst['name'], inst['activation_url'], inst['valid_parameters'], _filter['filter_name']))
        return ret


class Filters(tabs.TableTab):
    table_classes = (filter_tables.StorletFilterTable, filter_tables.NativeFilterTable)
    name = _("Filters")
    slug = "filters_table"
    template_name = "crystal/filters/filters/_detail.html"
    response = None
    preload = False

    def get_storlet_filters_data(self):
        try:
            if not self.response:
                self.response = api.fil_list_filters(self.request)
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
                ret.append(filters_models.Filter(inst['id'], inst['filter_name'], inst['dsl_name'], inst['filter_type'], inst['language'], inst['dependencies'],
                                                 inst['interface_version'], inst['main'], inst['has_reverse'],
                                                 inst['execution_server'], inst['execution_server_reverse'],
                                                 inst['is_pre_put'], inst['is_post_put'], inst['is_pre_get'], inst['is_post_get']))
        return ret

    def get_native_filters_data(self):
        try:
            if not self.response:
                self.response = api.fil_list_filters(self.request)
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
                ret.append(filters_models.Filter(inst['id'], inst['filter_name'], inst['dsl_name'], inst['filter_type'], inst['language'], None,
                                                 None, inst['main'], inst['has_reverse'],
                                                 inst['execution_server'], inst['execution_server_reverse'],
                                                 inst['is_pre_put'], inst['is_post_put'], inst['is_pre_get'], inst['is_post_get']))
        return ret


class Dependencies(tabs.TableTab):
    table_classes = (dependency_tables.DependenciesTable,)
    name = _("Dependencies")
    slug = "dependencies_table"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_dependencies_data(self):
        try:
            response = api.fil_list_dependencies(self.request)
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


class Groups(tabs.TableTab):
    table_classes = (group_tables.GroupsTable,)
    name = _("Groups")
    slug = "groups_table"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_groups_data(self):
        ret = []
        try:
            response = api.dsl_get_all_tenants_groups(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get project groups.'
                raise sdsexception.SdsException(error_message)

            instances = eval(strobj)
            for k, v in instances.items():
                projects = ', '.join(v)
                ret.append(group_models.Group(k, projects))
        except Exception as e:
            exceptions.handle(self.request, e.message)
        return ret


class FiltersTabs(tabs.TabGroup):
    slug = "filters_tabs"
    tabs = (Filters, RegistryTab, Groups,)
    sticky = True

