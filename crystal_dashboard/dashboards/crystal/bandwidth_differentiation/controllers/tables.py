import json

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from keystoneclient.exceptions import Conflict

from horizon import exceptions
from horizon import forms
from horizon import tables
from models import Controller
from crystal_dashboard.api import crystal as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class UpdateCell(tables.UpdateAction):
    def allowed(self, request, controller, cell):
        return cell.column.name == "enabled"

    def update_cell(self, request, datum, id, cell_name, new_cell_value):
        try:
            # updating changed value by new value
            response = api.dsl_get_global_controller(request, id)
            data = json.loads(response.text)
            data[cell_name] = new_cell_value
            api.dsl_update_global_controller(request, id, data)
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
        response = api.dsl_get_global_controller(request, id)
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
    success_url = "horizon:crystal:bandwidth_differentiation:index"

    def delete(self, request, obj_id):
        try:
            response = api.dsl_delete_global_controller(request, obj_id)
            if 200 <= response.status_code < 300:
                pass
                # messages.success(request, _("Successfully deleted controller: %s") % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:bandwidth_differentiation:index")
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
    success_url = "horizon:crystal:bandwidth_differentiation:index"

    def allowed(self, request, instance):
        return (instance is None) or (instance.enabled in ("False", False))

    def action(self, request, datum_id):
        data = {'enabled': True}
        api.dsl_update_global_controller(request, datum_id, data)


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

    name = "disable_Controller"
    success_url = "horizon:crystal:bandwidth_differentiation:index"

    def allowed(self, request, instance):
        return (instance is None) or (instance.enabled in ("True", True))

    def action(self, request, datum_id):
        data = {'enabled': False}
        api.dsl_update_global_controller(request, datum_id, data)


class DisableMultipleControllers(DisableController):
    def handle(self, table, request, obj_ids):
        allowed_ids = []
        for obj_id in obj_ids:
            if table.get_object_by_id(obj_id).enabled:
                allowed_ids.append(obj_id)

        # Call to super with allowed_ids
        return super(DisableMultipleControllers, self).handle(table, request, allowed_ids)

    name = "disable_multiple_metric_modules"


class MyGETControllerFilterAction(tables.FilterAction):
    name = "mygetfilter"


class CreateGETController(tables.LinkAction):
    name = "create_get"
    verbose_name = _("Create Controller")
    url = "horizon:crystal:bandwidth_differentiation:controllers:create_get_controller"
    classes = ("ajax-modal",)
    icon = "plus"


class ControllersGETTable(tables.DataTable):
    # id = tables.Column("id", verbose_name=_("ID"))
    controller_name = tables.Column("controller_name", verbose_name=_("Name"))
    class_name = tables.Column("class_name", verbose_name=_("Class name"))
    enabled = tables.Column("enabled", verbose_name=_("Enabled"), form_field=forms.ChoiceField(choices=[('True', _('True')), ('False', _('False'))]),
                            update_action=UpdateCell)

    class Meta:
        name = "get_controllers"
        verbose_name = _("GET Controllers")
        table_actions_menu = (EnableMultipleControllers, DisableMultipleControllers,)
        table_actions = (MyGETControllerFilterAction, CreateGETController, DeleteMultipleControllers,)
        row_actions = (EnableController, DisableController, DeleteController,)
        row_class = UpdateRow
        hidden_title = False


class MyPUTControllerFilterAction(tables.FilterAction):
    name = "myputfilter"


class CreatePUTController(tables.LinkAction):
    name = "create_put"
    verbose_name = _("Create Controller")
    url = "horizon:crystal:bandwidth_differentiation:controllers:create_put_controller"
    classes = ("ajax-modal",)
    icon = "plus"


class ControllersPUTTable(tables.DataTable):
    # id = tables.Column("id", verbose_name=_("ID"))
    controller_name = tables.Column("controller_name", verbose_name=_("Name"))
    class_name = tables.Column("class_name", verbose_name=_("Class name"))
    enabled = tables.Column("enabled", verbose_name=_("Enabled"), form_field=forms.ChoiceField(choices=[('True', _('True')), ('False', _('False'))]),
                            update_action=UpdateCell)

    class Meta:
        name = "put_controllers"
        verbose_name = _("PUT Controllers")
        table_actions_menu = (EnableMultipleControllers, DisableMultipleControllers,)
        table_actions = (MyPUTControllerFilterAction, CreatePUTController, DeleteMultipleControllers,)
        row_actions = (EnableController, DisableController, DeleteController,)
        row_class = UpdateRow
        hidden_title = False


class MyReplicationControllerFilterAction(tables.FilterAction):
    name = "myreplicationfilter"


class CreateReplicationController(tables.LinkAction):
    name = "create_replication"
    verbose_name = _("Create Controller")
    url = "horizon:crystal:bandwidth_differentiation:controllers:create_replication_controller"
    classes = ("ajax-modal",)
    icon = "plus"


class ControllersReplicationTable(tables.DataTable):
    # id = tables.Column("id", verbose_name=_("ID"))
    controller_name = tables.Column("controller_name", verbose_name=_("Name"))
    class_name = tables.Column("class_name", verbose_name=_("Class name"))
    enabled = tables.Column("enabled", verbose_name=_("Enabled"), form_field=forms.ChoiceField(choices=[('True', _('True')), ('False', _('False'))]),
                            update_action=UpdateCell)

    class Meta:
        name = "replication_controllers"
        verbose_name = _("Replication Controllers")
        table_actions_menu = (EnableMultipleControllers, DisableMultipleControllers,)
        table_actions = (MyReplicationControllerFilterAction, CreateReplicationController, DeleteMultipleControllers,)
        row_actions = (EnableController, DisableController, DeleteController,)
        row_class = UpdateRow
        hidden_title = False
