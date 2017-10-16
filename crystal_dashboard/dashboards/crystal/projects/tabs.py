import json
from horizon import exceptions
from horizon import messages
from horizon import tabs
from crystal_dashboard.api import projects as crystal_api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from crystal_dashboard.dashboards.crystal.projects.projects import tables as project_tables
from crystal_dashboard.dashboards.crystal.projects.projects.models import CrystalProject
from crystal_dashboard.dashboards.crystal.projects.groups import models as group_models
from crystal_dashboard.dashboards.crystal.projects.groups import tables as group_tables
from django.conf import settings
from openstack_dashboard import api
from openstack_dashboard import policy
from openstack_dashboard.utils import identity
from django.utils.translation import ugettext_lazy as _


class Groups(tabs.TableTab):
    table_classes = (group_tables.GroupsTable,)
    name = _("Groups")
    slug = "groups_table"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_groups_data(self):
        ret = []
        try:
            response = crystal_api.get_all_project_groups(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get project groups.'
                raise sdsexception.SdsException(error_message)
    
            groups = json.loads(strobj)    
            for group in groups:
                projects = 'Projects: ' + ', '.join(group['attached_projects'])
                ret.append(group_models.Group(group['id'], group['name'], projects))
        except Exception as e:
            exceptions.handle(self.request, e.message)
        return ret


class Projects(tabs.TableTab):
    table_classes = (project_tables.TenantsTable,)
    name = _("Projects")
    slug = "projects_table"
    template_name = "crystal/projects/_detail.html"
    response = None
    preload = False

    def _get_tenants_table(self):
        return self._tables['tenants']

    def _get_filter(self):
        filter = None
        if hasattr(self.request, "_post"):
            filter_value = self.request._post['tenants__filter__q']
            if filter_value:
                filter_field = self.request._post['tenants__filter__q_field']
                filter = {filter_field:
                          filter_value}
        return filter

    def get_tenants_data(self):
        tenants = []

        marker = self.request.GET.get(
            project_tables.TenantsTable._meta.pagination_param, None)
        self._more = False

        filters = self._get_filter()

        if policy.check((("crystal", "crystal:list_projects"),),
                        self.request):

            # If filter_first is set and if there are not other filters
            # selected, then search criteria must be provided and
            # return an empty list
            filter_first = getattr(settings, 'FILTER_DATA_FIRST', {})
            if filter_first.get('crystal.projects', False):
                return tenants

            domain_id = identity.get_domain_id_for_operation(self.request)
            try:
                tenants, self._more = api.keystone.tenant_list(
                    self.request,
                    domain=domain_id,
                    paginate=True,
                    filters=filters,
                    marker=marker)
            except Exception:
                exceptions.handle(self.request,
                                  _("Unable to retrieve project list."))
        elif policy.check((("crystal", "crystal:list_user_projects"),),
                          self.request):
            try:
                tenants, self._more = api.keystone.tenant_list(
                    self.request,
                    user=self.request.user.id,
                    paginate=True,
                    marker=marker,
                    filters=filters,
                    admin=False)
            except Exception:
                exceptions.handle(self.request,
                                  _("Unable to retrieve project information."))
        else:
            msg = \
                _("Insufficient privilege level to view project information.")
            messages.info(self.request, msg)

        if api.keystone.VERSIONS.active >= 3:
            domain_lookup = api.keystone.domain_lookup(self.request)
            for t in tenants:
                t.domain_name = domain_lookup.get(t.domain_id)

        enabled_crystal_projects = json.loads(crystal_api.list_projects_crystal_enabled(self.request).text)
        projects = []

        for tenant in tenants:
            if tenant.id in enabled_crystal_projects:
                crystal_enabled = True
            else:
                crystal_enabled = False
            project = CrystalProject(tenant.id, tenant.name,
                                     tenant.description, tenant.domain_id,
                                     tenant.enabled, crystal_enabled)
            projects.append(project)
        return projects


class ProjectsTabs(tabs.TabGroup):
    slug = "project_tabs"
    tabs = (Projects, Groups,)
    sticky = True
