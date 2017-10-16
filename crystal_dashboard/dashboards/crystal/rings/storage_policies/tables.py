from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from django.core.urlresolvers import reverse_lazy
from horizon import exceptions
from horizon import messages
from horizon import tables
from horizon import forms
import json

from crystal_dashboard.dashboards.crystal.rings.storage_policies import models as storage_policies_models
from crystal_dashboard.api import swift as api


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateStoragePolicy(tables.LinkAction):
    name = "create_storage_policy"
    verbose_name = _("Create Replication Policy")
    url = "horizon:crystal:rings:storage_policies:create_storage_policy"
    classes = ("ajax-modal",)
    icon = "plus"


class CreateECStoragePolicy(tables.LinkAction):
    name = "create_ec_storage_policy"
    verbose_name = _("Create EC Policy")
    url = "horizon:crystal:rings:storage_policies:create_ec_storage_policy"
    classes = ("ajax-modal",)
    icon = "plus"


class LoadSwiftPolicies(tables.LinkAction):
    name = "load_swift_policies"
    verbose_name = _("Load Swift Policies")
    url = "horizon:crystal:rings:storage_policies:load_swift_policies"
    classes = ("ajax-modal",)
    icon = "plus"


class ManageDisksLink(tables.LinkAction):
    name = "users"
    verbose_name = _("Manage Devices")
    url = "horizon:crystal:rings:storage_policies:devices"
    icon = "pencil"

    def get_link_url(self, datum=None):
        return reverse(self.url, kwargs={'policy_id': self.datum.id})


class UpdateCell(tables.UpdateAction):

    def allowed(self, request, project, cell):
        return True

    def update_cell(self, request, datum, obj_id, cell_name, new_cell_value):
        try:
            api.swift_edit_storage_policy(request, obj_id, {cell_name: new_cell_value})
        except Exception:
            exceptions.handle(request, ignore=True)
            return False
        return True


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, obj_id):
        response = api.swift_storage_policy_detail(request, obj_id)
        inst = json.loads(response.text)
        parameters = ', '.join([key.replace('_', ' ').title()+':'+inst[key] for key in inst.keys() if key not in ['id', 'name', 'policy_type', 'default', 'devices', 'deprecated', 'deployed']])
        policy = storage_policies_models.StoragePolicy(inst['id'], inst['name'], inst['policy_type'], inst['default'], parameters, inst['deprecated'], inst['deployed'], inst['devices'])

        return policy


class StoragePolicyTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    type = tables.Column('type', verbose_name=_("Type"))
    default = tables.Column('default', verbose_name=_("Default"),
                            form_field=forms.ChoiceField(choices=[('yes', _('Yes')), ('no', _('No'))]), update_action=UpdateCell)
    parameters = tables.Column('parameters', verbose_name=_("Parameters"))
    deprecated = tables.Column('deprecated', verbose_name=_("Deprecated"))
    devices = tables.Column('devices', verbose_name=_("Devices"))
    deployed = tables.Column('deployed', verbose_name=_("Deployed"))

    class Meta:
        name = "storagepolicies"
        verbose_name = _("Storage Policies")
        table_actions = (MyFilterAction, CreateStoragePolicy, CreateECStoragePolicy, LoadSwiftPolicies,)
        row_actions = (ManageDisksLink,)
        row_class = UpdateRow


class AddDisk(tables.LinkAction):
    name = "add_disk"
    verbose_name = _("Add Device")
    url = "horizon:crystal:rings:storage_policies:add_devices"
    classes = ("ajax-modal",)
    icon = "plus"

    def get_link_url(self, datum=None):
        return reverse(self.url, kwargs=self.table.kwargs)


class DeleteDisk(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete disk",
            u"Delete disks",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Disk deleted",
            u"Disks deleted",
            count
        )

    name = "delete"
    success_url = "horizon:crystal:rings:storage_policies:devices"

    def delete(self, request, obj_id):
        policy_id = self.table.kwargs['policy_id']
        try:
            response = api.swift_remove_disk_storage_policy(request, policy_id, obj_id)
            if not 200 <= response.status_code < 300:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:rings:storage_policies:devices")
            error_message = "Unable to remove disk.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
        
        
    def get_success_url(self, request=None):
        policy_id = self.table.kwargs.get('policy_id', None)
        return reverse(self.success_url, args=[policy_id])


class ManageDisksTable(tables.DataTable):
    storage_node = tables.WrappingColumn('storage_node', verbose_name=_('Storage Node'))
    region = tables.Column('region', verbose_name="Region")
    zone = tables.Column('zone', verbose_name="Zone")
    device = tables.Column('device', verbose_name="Device")
    size_occupied = tables.Column('size_occupied', verbose_name="Size Occupied")
    size = tables.Column('size', verbose_name="Total Size")

    class Meta(object):
        name = "diskstable"
        verbose_name = _("Devices")
        table_actions = (MyFilterAction, AddDisk, DeleteDisk)


class AddDisksAction(tables.BatchAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Add Device",
            u"Add Devices",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Added Device",
            u"Added Devices",
            count
        )

    name = "add"
    icon = "plus"
    requires_input = True
    success_url = "horizon:crystal:rings:storage_policies:devices"

    def action(self, request, obj_id):
        policy_id = self.table.kwargs['policy_id']
        try:
            response = api.swift_add_disk_storage_policy(request, policy_id, obj_id)
            if not 200 <= response.status_code < 300:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:rings:storage_policies:devices")
            error_message = "Unable to add disk.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)

    def get_success_url(self, request=None):
        policy_id = self.table.kwargs.get('policy_id', None)
        return reverse(self.success_url, args=[policy_id])


class AddDisksTable(ManageDisksTable):

    class Meta(object):
        name = "add_devices_table"
        verbose_name = _("Devices")
        table_actions = (MyFilterAction, AddDisksAction,)
