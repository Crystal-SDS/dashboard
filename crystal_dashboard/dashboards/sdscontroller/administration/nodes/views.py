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

"""
Views for managing object types.
"""
import json

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller.administration.nodes import forms as nodes_forms


class UpdateNodeView(forms.ModalFormView):
    form_class = nodes_forms.UpdateNode
    form_id = "update_node_form"
    modal_header = _("Update Node")
    submit_label = _("Update Node")
    submit_url = "horizon:sdscontroller:administration:nodes:update"
    template_name = "sdscontroller/administration/nodes/update.html"
    context_object_name = 'node'
    success_url = reverse_lazy('horizon:sdscontroller:administration:index')
    page_title = _("Update Node")

    def get_context_data(self, **kwargs):
        context = super(UpdateNodeView, self).get_context_data(**kwargs)
        context['node_id'] = self.kwargs['node_id']
        args = (self.kwargs['node_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        name = self.kwargs['node_id']
        try:
            object_type = api.swift_get_node_detail(self.request, name)
            return object_type
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve node details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        node = self._get_object()
        node_id = self.kwargs['node_id']
        initial = json.loads(node.text)
        initial['id'] = node_id
        return initial
