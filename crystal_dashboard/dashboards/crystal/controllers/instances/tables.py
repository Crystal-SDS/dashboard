from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from horizon import exceptions
from horizon import forms
from horizon import tables
from crystal_dashboard.api import controllers as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


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


class UpdateInstance(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, datum=None):
        base_url = reverse("horizon:crystal:controllers:instances:update_instance", kwargs={'id': datum.id})
        return base_url


class StartInstance(tables.BatchAction):

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Start",
            u"Start Instance",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Start",
            u"Start Instance",
            count
        )

    name = "start_instance"
    success_url = "horizon:crystal:controllers:index"

    def allowed(self, request, instance):
        return (instance is None) or (instance.status == "Stopped")

    def action(self, request, datum_id):
        try:
            response = api.update_instance(request, datum_id, {'status': 'Running'})
            if 200 <= response.status_code < 300:
                messages.success(request, _("Instance successfully started."))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:controllers:index")
            error_message = "Unable to start instance.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)



class StopInstance(tables.BatchAction):

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Stop",
            u"Stop Instance",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Stop",
            u"Stop Instance",
            count
        )

    name = "stop_instance"
    success_url = "horizon:crystal:controllers:index"

    def allowed(self, request, instance):
        return (instance is None) or (instance.status == "Running")

    def action(self, request, datum_id):
        try:
            response = api.update_instance(request, datum_id, {'status': 'Stopped'})
            if 200 <= response.status_code < 300:
                messages.success(request, _("Instance successfully stopped."))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:controllers:index")
            error_message = "Unable to stop instance.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class InstancesTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"))
    controller = tables.Column("controller", verbose_name=_("Controller"))
    parameters = tables.Column("parameters", verbose_name=_("Parameters"))
    description = tables.Column("description", verbose_name=_("Description"))
    status = tables.Column("status", verbose_name=_("Status"))

    class Meta:
        name = "instances"
        verbose_name = _("Instances")
        table_actions = (MyInstanceFilterAction, CreateInstance, DeleteMultipleInstances,)
        row_actions = (StartInstance, StopInstance, UpdateInstance, DeleteInstance,)
