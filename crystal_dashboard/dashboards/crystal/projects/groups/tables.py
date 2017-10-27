from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from django.core.urlresolvers import reverse
from horizon import tables
from horizon import exceptions


from crystal_dashboard.api import projects as api


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateGroup(tables.LinkAction):
    name = "create_group"
    verbose_name = _("Create Group")
    url = "horizon:crystal:projects:groups:create"
    classes = ("ajax-modal",)
    icon = "plus"


class UpdateGroup(tables.LinkAction):
    name = "update_group"
    verbose_name = _("Edit")
    url = "horizon:crystal:projects:groups:update"
    classes = ("ajax-modal",)
    icon = "plus"


class DeleteGroup(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Group",
            u"Delete Groups",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Group",
            u"Deleted Groups",
            count
        )

    name = "delete_group"
    success_url = "horizon:crystal:projects:index"

    def delete(self, request, obj_id):
        try:
            response = api.delete_project_group(request, obj_id)
            if 200 <= response.status_code < 300:
                pass
                # messages.success(request, _("Successfully deleted controller: %s") % obj_id)
            else:
                raise ValueError(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:projects:index")
            error_message = "Unable to remove group.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class DeleteMultipleGroups(DeleteGroup):
    name = "delete_multiple_groups"


class GroupsTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    tenants = tables.Column('projects', verbose_name=_("Projects"))

    class Meta:
        name = "groups"
        verbose_name = _("Groups")
        table_actions = (MyFilterAction, CreateGroup, DeleteMultipleGroups)
        row_actions = (UpdateGroup, DeleteGroup)
