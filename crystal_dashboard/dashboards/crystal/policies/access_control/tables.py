import json

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from keystoneclient.exceptions import Conflict

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon import tables
from models import AccessControlPolicy
from crystal_dashboard.api import policies as api
from crystal_dashboard.dashboards.crystal import common
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateAccessControlPolicy(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Policy")
    url = "horizon:crystal:policies:access_control:create"
    classes = ("ajax-modal",)
    icon = "plus"


class UpdateAccessControlPolicy(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, datum=None):
        base_url = reverse("horizon:crystal:policies:access_control:update", kwargs={"policy_id": datum.id})
        return base_url


class DeleteAccessControlPolicy(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Policy",
            u"Delete Policies",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Policy",
            u"Deleted Policies",
            count
        )

    name = "delete_sla"
    success_url = "horizon:crystal:policies:index"

    def delete(self, request, obj_id):
        try:
            success = True
            error_msg = ''
            response = api.delete_access_control(request, obj_id)
            if 200 <= response.status_code < 300:
                pass
                # messages.success(request, _("Successfully deleted sla: %s") % obj_id)
            else:
                success = False
                error_msg = response.text
            if not success:
                raise sdsexception.SdsException(error_msg)
        except Exception as ex:
            redirect = reverse("horizon:crystal:policies:index")
            error_message = "Unable to remove access control policy.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class DeleteMultipleAccessControlPolicies(DeleteAccessControlPolicy):
    name = "delete_multiple_policies"


class AccessControlTable(tables.DataTable):
    target_name = tables.Column('target_name', verbose_name=_("Target"))
    user = tables.Column('user', verbose_name=_("User"))
    write = tables.Column('write', verbose_name="Write")
    read = tables.Column('read', verbose_name=_("Read"))
    object_type = tables.Column('object_type', verbose_name=_("Object Type"))
    object_tag = tables.Column('object_tag', verbose_name=_("Object Tag"))

    class Meta:
        name = "access_control_policies"
        verbose_name = _("Access Control")
        table_actions = (MyFilterAction, CreateAccessControlPolicy, DeleteMultipleAccessControlPolicies)
        row_actions = (DeleteAccessControlPolicy,)
        hidden_title = False
