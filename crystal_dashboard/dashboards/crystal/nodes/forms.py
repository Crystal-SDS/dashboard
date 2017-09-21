"""
Forms for managing nodes.
"""
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from crystal_dashboard.api import crystal as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class UpdateNode(forms.SelfHandlingForm):
    filter_list = []

    id = forms.CharField(max_length=255,
                         label=_("Hostname"),
                         widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    server = forms.CharField(max_length=255,
                             label=_("Server Type"),
                             widget=forms.HiddenInput())

    ssh_username = forms.CharField(max_length=255,
                                   label=_("SSH User name"))

    ssh_password = forms.CharField(label=_("SSH Password"),
                                   widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        super(UpdateNode, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            node_id = data['id']
            server = data['server']
            data.pop('id', None)
            response = api.swift_update_node(request, server, node_id, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully updated node: %s') % node_id)
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:nodes:index")
            error_message = "Unable to update node.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
