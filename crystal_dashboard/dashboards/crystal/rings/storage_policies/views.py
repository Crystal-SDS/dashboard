"""
Views for managing Ring & Storage Policies.
"""
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse

import json
from horizon import forms
from horizon import workflows
from horizon import tables
from horizon import exceptions

from crystal_dashboard.dashboards.crystal.rings.storage_policies import forms as storage_policies_forms
from crystal_dashboard.dashboards.crystal.rings.storage_policies import tables as storage_policies_tables
from crystal_dashboard.dashboards.crystal.rings.storage_policies import models
from crystal_dashboard.api import swift as api


class CreateStoragePolicy(forms.ModalFormView):
    form_class = storage_policies_forms.CreateStoragePolicy
    form_id = "create_storage_policy_form"
    
    modal_header = _("Create a Storage Policy")
    submit_label = _("Create Storage Policy")
    submit_url = reverse_lazy('horizon:crystal:rings:storage_policies:create_storage_policy')
    template_name = "crystal/rings/storage_policies/create_storage_policy.html"
    context_object_name = 'storage_policy'
    success_url = reverse_lazy('horizon:crystal:rings:index')
    page_title = _("Create a Storage Policy")
    
class UpdateStoragePolicy(forms.ModalFormView):
    form_class = storage_policies_forms.UpdateStoragePolicy
    form_id = "update_storage_policy_form"
    
    modal_header = _("Update a Storage Policy")
    submit_label = _("Update Storage Policy")
    template_name = "crystal/rings/storage_policies/update_storage_policy.html"
    context_object_name = 'storage_policy'
    submit_url = 'horizon:crystal:rings:storage_policies:update_storage_policy'
    success_url = reverse_lazy('horizon:crystal:rings:index')
    page_title = _("Update a Storage Policy")
    
    def get_context_data(self, **kwargs):
        context = super(UpdateStoragePolicy, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        args = (self.kwargs['id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def _get_object(self, *args, **kwargs):
        storage_policy_id = self.kwargs['id']
        try:
            filter = api.swift_storage_policy_detail(self.request, storage_policy_id)
            return filter
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve controller details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        storage_policy = self._get_object()
        initial = json.loads(storage_policy.text)
        return initial



class CreateECStoragePolicy(forms.ModalFormView):
    form_class = storage_policies_forms.CreateECStoragePolicy
    form_id = "create_ec_storage_policy_form"

    modal_header = _("Create a EC Storage Policy")
    submit_label = _("Create EC Storage Policy")
    submit_url = reverse_lazy('horizon:crystal:rings:storage_policies:create_ec_storage_policy')
    template_name = "crystal/rings/storage_policies/create_ec_storage_policy.html"
    context_object_name = 'storage_policy'
    success_url = reverse_lazy('horizon:crystal:rings:index')
    page_title = _("Create a EC Storage Policy")


class ManageDisksView(tables.DataTableView):
    table_class = storage_policies_tables.ManageDisksTable
    template_name = "crystal/rings/storage_policies/manage_disks.html"
    page_title = _("Device Management")

    def get_context_data(self, **kwargs):
        context = super(ManageDisksView, self).get_context_data(**kwargs)
        context['policy_id'] = self.kwargs['policy_id']
        return context

    def get_data(self):
        policy_id = self.kwargs['policy_id']
        devices = []
        try:
            storage_node = json.loads((api.swift_storage_policy_detail(self.request, policy_id)).text)
            for device in storage_node['devices']:
                total = device['size']
                occuped = (total - device['free'])
                node_name, device_name = device['id'].split(':')
                devices.append(models.Device(device['id'], node_name, device['region'], device['zone'], device_name, occuped, total))

        except Exception:
            exceptions.handle(self.request, _('Unable to retrieve devices.'))
        return devices


class AddDisksView(forms.ModalFormMixin, tables.DataTableView):

    template_name = "crystal/rings/storage_policies/add_disk.html"
    ajax_template_name = "crystal/rings/storage_policies/_add_disk.html"
    table_class = storage_policies_tables.AddDisksTable

    def get_context_data(self, **kwargs):
        context = super(AddDisksView, self).get_context_data(**kwargs)
        context['policy_id'] = self.kwargs['policy_id']
        return context

    def get_data(self):
        devices_objects = []
        try:
            devices = json.loads(api.swift_available_disks_storage_policy(self.request, self.kwargs['policy_id']).text)
            for device in devices:
                total = device['size']
                occuped = (total - device['free'])
                controller_name, device_name = device['id'].split(':')
                devices_objects.append(models.Device(device['id'], controller_name, device['region'], device['zone'], device_name, occuped, total))
        except Exception:
            exceptions.handle(self.request, _('Unable to retrieve devices.'))
        return devices_objects
