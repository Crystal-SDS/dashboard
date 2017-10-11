from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from keystoneclient.exceptions import Conflict
from horizon import exceptions
from horizon import forms
from horizon import tables
from models import Controller
import json
from crystal_dashboard.api import controllers as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class UpdateCell(tables.UpdateAction):
    def allowed(self, request, controller, cell):
        return cell.column.name == "enabled"

    def update_cell(self, request, datum, id, cell_name, new_cell_value):
        try:
            # updating changed value by new value
            response = api.get_controller(request, id)
            data = json.loads(response.text)
            data[cell_name] = new_cell_value
            api.update_controller(request, id, data)
        except Conflict:
            # Returning a nice error message about name conflict. The message
            # from exception is not that clear for the user
            message = _("Can't change value")
            raise ValidationError(message)
        except Exception:
            exceptions.handle(request, ignore=True)
            return False
        return True


class UpdateController(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, datum=None):
        base_url = reverse("horizon:crystal:controllers:controllers:update_controller", kwargs={'id': datum.id})
        return base_url


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, id):
        response = api.get_controller(request, id)
        data = json.loads(response.text)

        controller = Controller(data["id"], data["controller_name"], data["class_name"], data["enabled"])
        return controller


class DeleteController(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Controller",
            u"Delete Controllers",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Controller",
            u"Deleted Controllers",
            count
        )

    name = "delete_controller"
    success_url = "horizon:crystal:controllers:index"

    def delete(self, request, obj_id):
        try:
            response = api.delete_controller(request, obj_id)
            if 200 <= response.status_code < 300:
                pass
                # messages.success(request, _("Successfully deleted controller: %s") % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:controllers:index")
            error_message = "Unable to remove controller.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class DeleteMultipleControllers(DeleteController):
    name = "delete_multiple_controllers"


class MyControllerFilterAction(tables.FilterAction):
    name = "mycontrollerfilter"


class CreateController(tables.LinkAction):
    name = "create_controller"
    verbose_name = _("Create Controller")
    url = "horizon:crystal:controllers:controllers:create_controller"
    classes = ("ajax-modal",)
    icon = "plus"


class LaunchInstance(tables.LinkAction):
    name = "launch_instance"
    verbose_name = _("Create Instance")
    classes = ("ajax-modal",)
    icon = "plus"

    def get_link_url(self, datum=None):
        base_url = reverse("horizon:crystal:controllers:controllers:launch_instance", kwargs={'id': datum.id})
        return base_url


class ControllersTable(tables.DataTable):
    # id = tables.Column("id", verbose_name=_("ID"))
    controller_name = tables.Column("controller_name", verbose_name=_("Name"))
    class_name = tables.Column("class_name", verbose_name=_("Main Class"))
    valid_parameters = tables.Column("valid_parameters", verbose_name=_("Valid Parameters"))
    description = tables.Column("description", verbose_name=_("Description"))
    instances = tables.Column("instances", verbose_name=_("Instances"))

    class Meta:
        name = "controllers"
        verbose_name = _("Controllers")
        table_actions = (MyControllerFilterAction, CreateController, DeleteMultipleControllers,)
        row_actions = (LaunchInstance, UpdateController, DeleteController)
        row_class = UpdateRow
