import json

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon import tables
from crystal_dashboard.api import policies as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from crystal_dashboard.dashboards.crystal.policies.object_types.models import ObjectType


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateObjectType(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Object Type")
    url = "horizon:crystal:policies:object_types:create"
    classes = ("ajax-modal",)
    icon = "plus"


class UpdateObjectType(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, datum=None):
        base_url = reverse("horizon:crystal:policies:object_types:update", kwargs={'object_type_id': datum.id})
        return base_url


class DeleteObjectType(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Object Type",
            u"Delete Object Types",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Object Type deleted",
            u"Object Types deleted",
            count
        )

    name = "delete_object_type"
    success_url = "horizon:crystal:policies:index"

    def delete(self, request, obj_id):
        try:
            response = api.dsl_delete_object_type(request, obj_id)
            if 200 <= response.status_code < 300:
                pass
                # messages.success(request, _('Successfully deleted object type: %s') % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:policies:index")
            error_message = "Unable to delete object type.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)


class UpdateCell(tables.UpdateAction):
    def allowed(self, request, datum, cell):
        return cell.column.name == 'extensions'

    def update_cell(self, request, datum, obj_id,
                    cell_name, new_cell_value):
        # inline update object type info
        try:
            # updating changed value by new value
            if cell_name == 'extensions':
                extensions = [x.strip() for x in new_cell_value.split(',')]
                api.dsl_update_object_type(request, obj_id, extensions)
        except Exception:
            exceptions.handle(request, ignore=True)
            return False
        return True


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, name):
        response = api.dsl_get_object_type(request, name)
        data = json.loads(response.text)
        objectType = ObjectType(data["name"], ', '.join(data["types_list"]))
        return objectType


class ObjectTypesTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    extensions = tables.Column('extensions', verbose_name=_("Extensions"), form_field=forms.CharField(max_length=255),
                               update_action=UpdateCell)

    class Meta:
        name = "object_types"
        verbose_name = _("Object Types")
        row_class = UpdateRow
        table_actions = (MyFilterAction, CreateObjectType,)
        row_actions = (UpdateObjectType, DeleteObjectType, )
