from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from horizon import exceptions
from horizon import messages
from horizon import tables
from crystal_dashboard.api import crystal as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateStoragePolicy(tables.LinkAction):
    name = "create_storage_policy"
    verbose_name = _("Create new policy")
    url = "horizon:crystal:rings:storage_policies:create_storage_policy"
    classes = ("ajax-modal",)
    icon = "plus"


class CreateECStoragePolicy(tables.LinkAction):
    name = "create_ec_storage_policy"
    verbose_name = _("Create EC Storage Policy")
    url = "horizon:crystal:rings:storage_policies:create_ec_storage_policy"
    classes = ("ajax-modal",)
    icon = "plus"


class LoadSwiftPolicies(tables.LinkAction):
    name = "load_swift_policies"
    verbose_name = _("Load Swift Policies")
    url = "horizon:crystal:rings:storage_policies:load_swift_policies"
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
    success_url = "horizon:crystal:rings:index"

    def delete(self, request, obj_id):
        try:
            response = api.remove_storage_nodes(request, obj_id)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully deleted storage node: %s') % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:rings:index")
            error_message = "Unable to remove storage node.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class DeleteMultipleStorageNodes(DeleteStorageNode):
    name = "delete_multiple_storage_nodes"


class StoragePolicyTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    type = tables.Column('type', verbose_name=_("Type"))
    new_field = tables.Column('new_field', verbose_name=_("New Field"))

    class Meta:
        name = "storagepolicies"
        verbose_name = _("Storage Policies")
        table_actions = (MyFilterAction, CreateStoragePolicy, CreateECStoragePolicy, LoadSwiftPolicies, DeleteMultipleStorageNodes,)
