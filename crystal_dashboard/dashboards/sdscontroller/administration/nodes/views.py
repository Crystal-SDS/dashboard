"""
Views for managing Nodes.
"""
import json

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from crystal_dashboard.api import sds_controller as api
from crystal_dashboard.dashboards.sdscontroller.administration.nodes import forms as nodes_forms


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
        context['server'] = self.kwargs['server']
        args = (self.kwargs['server'], self.kwargs['node_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        node_id = self.kwargs['node_id']
        server = self.kwargs['server']
        try:
            object_type = api.swift_get_node_detail(self.request, server, node_id)
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
        initial['server'] = initial['type']
        return initial
