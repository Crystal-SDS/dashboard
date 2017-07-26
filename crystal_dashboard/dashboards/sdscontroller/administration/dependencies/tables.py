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
from models import Dependency
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class UploadDependency(tables.LinkAction):
    name = "upload"
    verbose_name = _("Upload Dependency")
    url = "horizon:sdscontroller:administration:dependencies:upload"
    classes = ("ajax-modal",)
    icon = "upload"


class UpdateDependency(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, datum=None):
        base_url = reverse("horizon:sdscontroller:administration:dependencies:update", kwargs={'dependency_id': datum.id})
        return base_url


class UpdateCell(tables.UpdateAction):
    def allowed(self, request, project, cell):
        return ((cell.column.name == 'version') or
                (cell.column.name == 'permissions'))

    def update_cell(self, request, datum, id, cell_name, new_cell_value):
        try:
            # updating changed value by new value
            response = api.fil_get_dependency_metadata(request, id)
            data = json.loads(response.text)
            data[cell_name] = new_cell_value

            # TODO: Check only the valid keys, delete the rest
            if 'id' in data:  # PUT does not allow this key
                del data['id']
            if 'path' in data:  # PUT does not allow this key
                del data['path']

            api.fil_update_dependency_metadata(request, id, data['version'], data['permissions'])
        except Conflict:
            # Returning a nice error message about name conflict. The message
            # from exception is not that clear for the user
            message = _("Cant change value")
            raise ValidationError(message)
        except Exception:
            exceptions.handle(request, ignore=True)
            return False
        return True


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, id):
        response = api.fil_get_dependency_metadata(request, id)
        data = json.loads(response.text)
        print(data)
        dependency = Dependency(data['id'], data['name'],
                                data['version'], data['permissions'])
        return dependency


class DeleteDependency(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Dependency",
            u"Delete Dependencies",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Dependency",
            u"Deleted Dependencies",
            count
        )

    name = "delete_dependency"
    success_url = "horizon:sdscontroller:administration:index"

    def delete(self, request, obj_id):
        try:
            response = api.fil_delete_dependency(request, obj_id)
            if 200 <= response.status_code < 300:
                pass
                # messages.success(request, _('Successfully deleted dependency: %s') % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to remove dependency.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)


class DeleteMultipleDependencies(DeleteDependency):
    name = "delete_multiple_dependencies"


class DependenciesTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    version = tables.Column('version', verbose_name=_("Version"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    permissions = tables.Column('permissions', verbose_name=_("Permissions"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)

    class Meta:
        name = "dependencies"
        verbose_name = _("Dependencies")
        table_actions = (MyFilterAction, UploadDependency, DeleteMultipleDependencies,)
        row_actions = (UpdateDependency, DeleteDependency,)
        row_class = UpdateRow
