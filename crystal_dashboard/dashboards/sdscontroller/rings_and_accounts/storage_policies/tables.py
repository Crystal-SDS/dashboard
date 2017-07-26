from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import exceptions
from horizon import messages
from horizon import tables
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateStoragePolicy(tables.LinkAction):
    name = "create_storage_policy"
    verbose_name = _("Create new policy")
    url = "horizon:sdscontroller:rings_and_accounts:storage_policies:create_storage_policy"
    classes = ("ajax-modal",)
    icon = "plus"

class CreateECStoragePolicy(tables.LinkAction):
    name = "create_ec_storage_policy"
    verbose_name = _("Create EC Storage Policy")
    url = "horizon:sdscontroller:rings_and_accounts:storage_policies:create_ec_storage_policy"
    classes = ("ajax-modal",)
    icon = "plus"

class BindStorageNode(tables.LinkAction):
    name = "bind_storage_node"
    verbose_name = _("Register Storage Node")
    url = "horizon:sdscontroller:rings_and_accounts:storage_policies:bind_storage_node"
    classes = ("ajax-modal",)
    icon = "plus"


class DeleteStorageNode(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Storage Node",
            u"Delete Storage Nodes",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Delete Storage Node",
            u"Delete Storage Nodes",
            count
        )

    name = "delete_storage_node"
    success_url = "horizon:sdscontroller:rings_and_accounts:index"

    def delete(self, request, obj_id):
        try:
            response = api.remove_storage_nodes(request, obj_id)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully deleted storage node: %s') % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:rings_and_accounts:index")
            error_message = "Unable to remove storage node.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class DeleteMultipleStorageNodes(DeleteStorageNode):
    name = "delete_multiple_storage_nodes"


class StoragePolicyTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    location = tables.Column('location', verbose_name=_("Location"))
    type = tables.Column('type', verbose_name=_("Type"))

    class Meta:
        name = "storagepolicies"
        verbose_name = _("Storage Policies")
        table_actions = (MyFilterAction, CreateStoragePolicy, CreateECStoragePolicy, BindStorageNode, DeleteMultipleStorageNodes,)
