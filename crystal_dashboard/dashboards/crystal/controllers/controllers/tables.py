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


class EnableController(tables.BatchAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Enable",
            u"Enable Controllers",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Enabled Controller",
            u"Enabled Controllers",
            count
        )

    name = "enable_Controller"
    success_url = "horizon:crystal:controllers:index"

    def allowed(self, request, instance):
        return (instance is None) or (instance.enabled in ("False", False))

    def action(self, request, datum_id):
        data = {'enabled': True}
        api.update_controller(request, datum_id, data)


class EnableMultipleControllers(EnableController):
    def handle(self, table, request, obj_ids):
        allowed_ids = []
        for obj_id in obj_ids:
            if not table.get_object_by_id(obj_id).enabled:
                allowed_ids.append(obj_id)

        # Call to super with allowed_ids
        return super(EnableMultipleControllers, self).handle(table, request, allowed_ids)

    name = "enable_multiple_Controllers"


class DisableController(tables.BatchAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Disable",
            u"Disable Controllers",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Disabled Controller",
            u"Disabled Controllers",
            count
        )

    name = "disable_dontroller"
    success_url = "horizon:crystal:controllers:index"

    def allowed(self, request, instance):
        return (instance is None) or (instance.enabled in ("True", True))

    def action(self, request, datum_id):
        data = {'enabled': False}
        api.update_controller(request, datum_id, data)


class DisableMultipleControllers(DisableController):
    def handle(self, table, request, obj_ids):
        allowed_ids = []
        for obj_id in obj_ids:
            if table.get_object_by_id(obj_id).enabled:
                allowed_ids.append(obj_id)

        # Call to super with allowed_ids
        return super(DisableMultipleControllers, self).handle(table, request, allowed_ids)

    name = "disable_multiple_metric_modules"


class MyControllerFilterAction(tables.FilterAction):
    name = "mycontrollerfilter"


class CreateController(tables.LinkAction):
    name = "create_controller"
    verbose_name = _("Create Controller")
    url = "horizon:crystal:controllers:controllers:create_controller"
    classes = ("ajax-modal",)
    icon = "plus"


class ControllersTable(tables.DataTable):
    # id = tables.Column("id", verbose_name=_("ID"))
    controller_name = tables.Column("controller_name", verbose_name=_("Name"))
    class_name = tables.Column("class_name", verbose_name=_("Main Class"))
    description = tables.Column("description", verbose_name=_("Description"))
    enabled = tables.Column("enabled", verbose_name=_("Enabled"), form_field=forms.ChoiceField(choices=[('True', _('True')), ('False', _('False'))]),
                            update_action=UpdateCell)

    class Meta:
        name = "controllers"
        verbose_name = _("Controllers")
        table_actions_menu = (EnableMultipleControllers, DisableMultipleControllers)
        table_actions = (MyControllerFilterAction, CreateController, DeleteMultipleControllers,)
        row_actions = (EnableController, DisableController, UpdateController, DeleteController)
        row_class = UpdateRow
