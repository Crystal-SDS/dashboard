# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
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
Views for managing Ring & Storage Policies.
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

from horizon import forms

from crystal_dashboard.dashboards.sdscontroller.rings_and_accounts.storage_policies import forms as storage_policies_forms


class CreateStoragePolicy(forms.ModalFormView):
    form_class = storage_policies_forms.CreateStoragePolicy
    form_id = "create_storage_policy_form"

    modal_header = _("Create a Storage Policy")
    submit_label = _("Create a Storage Policy")
    submit_url = reverse_lazy('horizon:sdscontroller:rings_and_accounts:storage_policies:create_storage_policy')
    template_name = "sdscontroller/rings_and_accounts/storage_policies/create_storage_policy.html"
    context_object_name = 'storage_policy'
    success_url = reverse_lazy('horizon:sdscontroller:rings_and_accounts:index')
    page_title = _("Create a Storage Policy")


class CreateECStoragePolicy(forms.ModalFormView):
    form_class = storage_policies_forms.CreateECStoragePolicy
    form_id = "create_ec_storage_policy_form"

    modal_header = _("Create a EC Storage Policy")
    submit_label = _("Create a EC Storage Policy")
    submit_url = reverse_lazy('horizon:sdscontroller:rings_and_accounts:storage_policies:create_ec_storage_policy')
    template_name = "sdscontroller/rings_and_accounts/storage_policies/create_ec_storage_policy.html"
    context_object_name = 'storage_policy'
    success_url = reverse_lazy('horizon:sdscontroller:rings_and_accounts:index')
    page_title = _("Create a Storage Policy")

class BindStorageNode(forms.ModalFormView):
    form_class = storage_policies_forms.BindStorageNode
    form_id = "bind_storage_node_form"

    modal_header = _("Registry Storage Node")
    submit_label = _("Registry Storage Node")
    submit_url = reverse_lazy('horizon:sdscontroller:rings_and_accounts:storage_policies:bind_storage_node')
    template_name = "sdscontroller/rings_and_accounts/storage_policies/bind_storage_node.html"
    context_object_name = 'storage_node'
    success_url = reverse_lazy('horizon:sdscontroller:rings_and_accounts:index')
    page_title = _("Registry Storage Node")