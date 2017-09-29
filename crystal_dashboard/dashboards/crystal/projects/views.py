import json
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import messages
from horizon import tables

from models import CrystalProject

from openstack_dashboard import api
from openstack_dashboard import policy

from crystal_dashboard.dashboards.crystal.projects \
    import tables as project_tables
from openstack_dashboard.utils import identity

from crystal_dashboard.api import projects as crystal_api

PROJECT_INFO_FIELDS = ("domain_id",
                       "domain_name",
                       "name",
                       "description",
                       "enabled",
                       "crystal_enabled",)

INDEX_URL = "horizon:crystal:projects:index"


class IndexView(tables.DataTableView):
    table_class = project_tables.TenantsTable
    template_name = 'crystal/projects/index.html'
    page_title = _("Projects")

    def needs_filter_first(self, table):
        return self._needs_filter_first

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        tenants = []
        marker = self.request.GET.get(
            project_tables.TenantsTable._meta.pagination_param, None)
        self._more = False
        filters = self.get_filters()

        self._needs_filter_first = False

        if policy.check((("crystal", "crystal:list_projects"),),
                        self.request):

            # If filter_first is set and if there are not other filters
            # selected, then search criteria must be provided and
            # return an empty list
            filter_first = getattr(settings, 'FILTER_DATA_FIRST', {})
            if filter_first.get('crystal.projects', False) and len(
                    filters) == 0:
                self._needs_filter_first = True
                self._more = False
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
