# Copyright 2012 Nebula, Inc.
# All rights reserved.

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

"""
Forms for managing nodes.
"""
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from crystal_dashboard.api import sds_controller as api
from crystal_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class UpdateNode(forms.SelfHandlingForm):
    filter_list = []

    id = forms.CharField(max_length=255,
                         label=_("Hostname"),
                         widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    ssh_username = forms.CharField(max_length=255,
                                   label=_("SSH User name"))

    ssh_password = forms.CharField(label=_("SSH Password"), widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        super(UpdateNode, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            node_id = data['id']
            data.pop('id', None)
            response = api.swift_update_node(request, node_id, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully updated node: %s') % node_id)
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to update node.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
