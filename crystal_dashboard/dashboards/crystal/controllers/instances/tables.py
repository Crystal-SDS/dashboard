from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from keystoneclient.exceptions import Conflict
from horizon import exceptions
from horizon import forms
from horizon import tables
from models import Instance
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


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, id):
        response = api.get_controller(request, id)
        data = json.loads(response.text)

        controller = Controller(data["id"], data["controller_name"], data["class_name"], data["enabled"])
        return controller

class DeleteInstance(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Instance",
            u"Delete Instances",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Instance",
            u"Deleted Instances",
            count
        )

    name = "delete_instance"
    success_url = "horizon:crystal:controllers:index"

    def delete(self, request, obj_id):
        try:
            response = api.delete_instance(request, obj_id)
            if 200 <= response.status_code < 300:
                pass
                # messages.success(request, _("Successfully deleted instance: %s") % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:controllers:index")
            error_message = "Unable to remove instance.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class DeleteMultipleInstances(DeleteInstance):
    name = "delete_multiple_instances"


class MyInstanceFilterAction(tables.FilterAction):
    name = "myinstancefilter"


class CreateInstance(tables.LinkAction):
    name = "create_instance"
    verbose_name = _("Create Instance")
    url = "horizon:crystal:controllers:instances:create_instance"
    classes = ("ajax-modal",)
    icon = "plus"


class InstancesTable(tables.DataTable):
    # id = tables.Column("id", verbose_name=_("ID"))
    instance_name = tables.Column("instance_name", verbose_name=_("Name"))
    controller = tables.Column("controller", verbose_name=_("Controller"))
    parameters = tables.Column("parameters", verbose_name=_("Parameters"))

    class Meta:
        name = "instances"
        verbose_name = _("Instances")
        table_actions = (MyInstanceFilterAction, CreateInstance, DeleteMultipleInstances,)
        row_class = UpdateRow
