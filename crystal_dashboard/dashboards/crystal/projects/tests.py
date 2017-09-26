# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.core.urlresolvers import reverse
from django import http
from django.test.utils import override_settings

from mox3.mox import IgnoreArg  # noqa
from mox3.mox import IsA  # noqa

from openstack_dashboard import api
from openstack_dashboard.dashboards.identity.projects import workflows
from openstack_dashboard.test import helpers as test
from openstack_dashboard.usage import quotas


INDEX_URL = reverse('horizon:crystal:projects:index')
USER_ROLE_PREFIX = workflows.PROJECT_USER_MEMBER_SLUG + "_role_"
GROUP_ROLE_PREFIX = workflows.PROJECT_GROUP_MEMBER_SLUG + "_role_"
PROJECT_DETAIL_URL = reverse('horizon:crystal:projects:detail', args=[1])


class TenantsViewTests(test.BaseAdminViewTests):
    @test.create_stubs({api.keystone: ('domain_get',
                                       'tenant_list',
                                       'domain_lookup'),
                        quotas: ('enabled_quotas',)})
    def test_index(self):
        domain = self.domains.get(id="1")
        filters = {}
        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 domain=None,
                                 paginate=True,
                                 filters=filters,
                                 marker=None) \
            .AndReturn([self.tenants.list(), False])
        api.keystone.domain_lookup(IgnoreArg()).AndReturn({domain.id:
                                                           domain.name})
        quotas.enabled_quotas(IsA(http.HttpRequest)).MultipleTimes()\
            .AndReturn(('instances',))
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'crystal/projects/index.html')
        self.assertItemsEqual(res.context['table'].data, self.tenants.list())

    @test.create_stubs({api.keystone: ('tenant_list',
                                       'get_effective_domain_id',
                                       'domain_lookup'),
                        quotas: ('enabled_quotas',)})
    def test_index_with_domain_context(self):
        domain = self.domains.get(id="1")
        filters = {}
        self.setSessionValues(domain_context=domain.id,
                              domain_context_name=domain.name)

        domain_tenants = [tenant for tenant in self.tenants.list()
                          if tenant.domain_id == domain.id]

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 domain=domain.id,
                                 paginate=True,
                                 marker=None,
                                 filters=filters) \
                    .AndReturn([domain_tenants, False])
        api.keystone.domain_lookup(IgnoreArg()).AndReturn({domain.id:
                                                           domain.name})
        quotas.enabled_quotas(IsA(http.HttpRequest)).AndReturn(('instances',))
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'crystal/projects/index.html')
        self.assertItemsEqual(res.context['table'].data, domain_tenants)
        self.assertContains(res, "<em>test_domain:</em>")

    @test.update_settings(FILTER_DATA_FIRST={'identity.projects': True})
    def test_index_with_filter_first(self):
        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'crystal/projects/index.html')
        projects = res.context['table'].data
        self.assertItemsEqual(projects, [])


class ProjectsViewNonAdminTests(test.TestCase):
    @override_settings(POLICY_CHECK_FUNCTION='openstack_auth.policy.check')
    @test.create_stubs({api.keystone: ('tenant_list',
                                       'domain_lookup')})
    def test_index(self):
        domain = self.domains.get(id="1")
        filters = {}
        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 user=self.user.id,
                                 paginate=True,
                                 marker=None,
                                 filters=filters,
                                 admin=False) \
            .AndReturn([self.tenants.list(), False])
        api.keystone.domain_lookup(IgnoreArg()).AndReturn({domain.id:
                                                           domain.name})
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'crystal/projects/index.html')
        self.assertItemsEqual(res.context['table'].data, self.tenants.list())
