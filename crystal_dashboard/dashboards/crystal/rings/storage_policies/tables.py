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
    verbose_name = _("Manage Disks")
    url = "horizon:crystal:rings:storage_policies:disks"
    icon = "pencil"

    def get_link_url(self, datum=None):
        return reverse(self.url, kwargs={'policy_id': self.datum.id})


class UpdateCell(tables.UpdateAction):

    def allowed(self, request, project, cell):
        return True

    def update_cell(self, request, datum, obj_id, cell_name, new_cell_value):
        try:
            print cell_name
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
        print inst

        parameters = ', '.join([inst[key] for key in inst.keys() if key not in ['id', 'name', 'policy_type', 'default', 'devices']])
        policy = storage_policies_models.StorageNode(obj_id, inst['name'], inst['policy_type'], inst['default'], 'Parameters: ' + parameters)

        return policy


class StoragePolicyTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    type = tables.Column('type', verbose_name=_("Type"))
    default = tables.Column('default', verbose_name=_("Default"),
                            form_field=forms.ChoiceField(choices=[('yes', _('yes')), ('no', _('no'))]), update_action=UpdateCell)
    parameters = tables.Column('parameters', verbose_name=_("Parameters"))

    class Meta:
        name = "storagepolicies"
        verbose_name = _("Storage Policies")
        table_actions = (MyFilterAction, CreateStoragePolicy, CreateECStoragePolicy, LoadSwiftPolicies,)
        row_actions = (ManageDisksLink,)
        row_class = UpdateRow


class AddNodesLink(tables.LinkAction):
    name = "add_user_link"
    verbose_name = _("Add Users")
    url = "horizon:crystal:rings:storage_policies:add_nodes"
    classes = ("ajax-modal",)
    icon = "plus"


class NodesTable(tables.DataTable):
    hostname = tables.WrappingColumn('hostname', verbose_name=_('Hostname'))
    ip = tables.Column('ip', verbose_name="IP")

    class Meta(object):
        name = "nodestable"
        verbose_name = _("Nodes")
        table_actions = (MyFilterAction, AddNodesLink)


class AddDisk(tables.LinkAction):
    name = "add_disk"
    verbose_name = _("Add Disk")
    url = "horizon:crystal:rings:storage_policies:add_disks"
    classes = ("ajax-modal",)
    icon = "plus"

    def get_link_url(self, datum=None):
        return reverse(self.url, kwargs=self.table.kwargs)


class DeleteDisk(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Region",
            u"Delete Regions",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Region deleted",
            u"Regions deleted",
            count
        )

    name = "delete"
    success_url = "horizon:crystal:rings:index"

    def delete(self, request, region_id):
        pass


class ManageDisksTable(tables.DataTable):
    storage_node = tables.WrappingColumn('storage_node', verbose_name=_('Storage Node'))
    device = tables.Column('device', verbose_name="Device")
    size_occupied = tables.Column('size_occupied', verbose_name="Size Occupied")
    size = tables.Column('size', verbose_name="Total Size")

    class Meta(object):
        name = "diskstable"
        verbose_name = _("Disks")
        table_actions = (MyFilterAction, AddDisk, DeleteDisk)


class AddDisksAction(tables.BatchAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Add Disk",
            u"Add Disks",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Added Disk",
            u"Added Disks",
            count
        )

    name = "add"
    icon = "plus"
    requires_input = True
    success_url = "horizon:crystal:rings:storage_policies:disks"

    def action(self, request, obj_id):
        policy_id = self.table.kwargs['policy_id']
        # TODO: Call controller to add disks

    def get_success_url(self, request=None):
        policy_id = self.table.kwargs.get('policy_id', None)
        return reverse(self.success_url, args=[policy_id])


class AddDisksTable(ManageDisksTable):

    class Meta(object):
        name = "group_non_members"
        verbose_name = _("Non-Members")
        table_actions = (MyFilterAction, AddDisksAction,)
