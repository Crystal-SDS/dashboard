# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.template import defaultfilters as filters
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from django import forms

from horizon import forms
from horizon import tables
from models import CrystalProject
from openstack_dashboard import api

from crystal_dashboard.api import projects as crystal_api


class EnableProject(tables.BatchAction):
    """
    Enable a Project
    """
    name = "enable_project"
    success_url = "horizon:crystal:projects:index"

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Enable",
            u"Enable Projects",
            count,
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Enabled",
            u"Enabled Projects",
            count,
        )

    def allowed(self, request, project):
        return (project is None) or not project.crystal_enabled

    def action(self, request, project_id):
        crystal_api.enable_crystal(request, project_id)



class DisableProject(tables.BatchAction):

    name = "disable_project"
    success_url = "horizon:crystal:projects:index"

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Disable",
            u"Disable Projects",
            count,
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Disabled",
            u"Disabled Projects",
            count,
        )

    def allowed(self, request, project):
        return (project is None) or project.crystal_enabled

    def action(self, request, project_id):
        crystal_api.disable_crystal(request, project_id)


class TenantFilterAction(tables.FilterAction):
    if api.keystone.VERSIONS.active < 3:
        filter_type = "query"
    else:
        filter_type = "server"
        filter_choices = (('name', _("Project Name ="), True),
                          ('id', _("Project ID ="), True),
                          ('enabled', _("Enabled ="), True, _('e.g. Yes/No')),
                          ('sds', _("Crystal Enabled ="), True, _('e.g. Yes/No')))


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, project_id):
        project_info = api.keystone.tenant_get(request, project_id, admin=True)
        response = crystal_api.is_crystal_project(request, project_id)
        if response.status_code == 200:
            crystal_enabled = True
        else:
            crystal_enabled = False
        project = CrystalProject(project_info.id, project_info.name,
                                 project_info.description, project_info.domain_id,
                                 project_info.enabled, crystal_enabled)
        return project



class TenantsTable(tables.DataTable):
    name = tables.WrappingColumn('name', verbose_name=_('Name'),
                                 form_field=forms.CharField(max_length=64))
    description = tables.Column(lambda obj: getattr(obj, 'description', None),
                                verbose_name=_('Description'),
                                form_field=forms.CharField(
                                    widget=forms.Textarea(attrs={'rows': 4}),
                                    required=False))
    id = tables.Column('id', verbose_name=_('Project ID'))

    if api.keystone.VERSIONS.active >= 3:
        domain_name = tables.Column(
            'domain_name', verbose_name=_('Domain Name'))

    enabled = tables.Column('enabled', verbose_name=_('Enabled'), status=True,
                            filters=(filters.yesno, filters.capfirst),
                            form_field=forms.BooleanField(
                                label=_('Enabled'),
                                required=False))

    crystal_enabled = tables.Column('crystal_enabled',
                                    verbose_name=_('Crystal Enabled'), status=True,
                                    filters=(filters.yesno, filters.capfirst),
                                    form_field=forms.BooleanField(
                                        label=_('Crystal Enabled'),
                                        required=False)
                                    )


    class Meta(object):
        name = "tenants"
        verbose_name = _("Projects")
        status_columns = ['crystal_enabled', ]
        row_actions = (EnableProject, DisableProject)
        table_actions = (TenantFilterAction,)
        pagination_param = "tenant_marker"
        row_class = UpdateRow