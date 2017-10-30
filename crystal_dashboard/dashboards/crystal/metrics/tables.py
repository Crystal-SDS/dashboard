import json

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from keystoneclient.exceptions import Conflict

from horizon import exceptions
from horizon import forms
from horizon import tables
from models import MetricModule
from crystal_dashboard.api import metrics as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class UploadMetricModule(tables.LinkAction):
    name = "upload_metric_module"
    verbose_name = _("Upload Workload Metric")
    url = "horizon:crystal:metrics:upload_metric_module"
    classes = ("ajax-modal",)
    icon = "upload"


class DownloadMetricModule(tables.LinkAction):
    name = "download"
    verbose_name = _("Download")
    icon = "download"

    def get_link_url(self, datum=None):
        base_url = reverse('horizon:crystal:metrics:download_metric_module', kwargs={'metric_module_id': datum.id})
        return base_url


class DeleteMetricModule(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete",
            u"Delete Metric Modules",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Metric Module",
            u"Deleted Metric Modules",
            count
        )

    name = "delete_metric_module"
    success_url = "horizon:crystal:metrics:index"

    def delete(self, request, obj_id):
        try:
            response = api.delete_metric_module(request, obj_id)
            if 200 <= response.status_code < 300:
                pass
                # messages.success(request, _('Successfully deleted metric module: %s') % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:metrics:index")
            error_message = "Unable to remove metric module.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class DeleteMultipleMetricModules(DeleteMetricModule):
    name = "delete_multiple_metric_modules"


class EnableMetricModule(tables.BatchAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Start",
            u"Start Metric Modules",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Start Metric Module",
            u"Start Metric Modules",
            count
        )

    name = "enable_metric_module"
    success_url = "horizon:crystal:metrics:index"

    def allowed(self, request, instance):
        return (instance is None) or (instance.status in ("Stopped", 'stopped'))

    def action(self, request, datum_id):
        data = {'status': 'Running'}
        api.update_metric_module_metadata(request, datum_id, data)


class EnableMultipleMetricModules(EnableMetricModule):
    def handle(self, table, request, obj_ids):
        allowed_ids = []
        for obj_id in obj_ids:
            if table.get_object_by_id(obj_id).status in ('Stopped', 'stopped'):
                allowed_ids.append(obj_id)

        # Call to super with allowed_ids
        return super(EnableMultipleMetricModules, self).handle(table, request, allowed_ids)

    name = "enable_multiple_metric_modules"


class DisableMetricModule(tables.BatchAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Stop",
            u"Stop Metric Modules",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Stoped Metric Module",
            u"Stoped Metric Modules",
            count
        )

    name = "disable_metric_module"
    success_url = "horizon:crystal:metrics:index"

    def allowed(self, request, instance):
        return (instance is None) or (instance.status in ("running", "Running"))

    def action(self, request, datum_id):
        data = {'status': 'Stopped'}
        api.update_metric_module_metadata(request, datum_id, data)


class DisableMultipleMetricModules(DisableMetricModule):
    def handle(self, table, request, obj_ids):
        allowed_ids = []
        for obj_id in obj_ids:
            if table.get_object_by_id(obj_id).status in ('Running', 'running'):
                allowed_ids.append(obj_id)

        # Call to super with allowed_ids
        return super(DisableMultipleMetricModules, self).handle(table, request, allowed_ids)

    name = "disable_multiple_metric_modules"


class UpdateMetricModule(tables.LinkAction):
    name = "update_metric_module"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, datum=None):
        base_url = reverse("horizon:crystal:metrics:update_metric_module", kwargs={'metric_module_id': datum.id})
        return base_url


class UpdateCell(tables.UpdateAction):
    def allowed(self, request, project, cell):
        return ((cell.column.name == 'execution_server') or (cell.column.name == 'class_name'))

    def update_cell(self, request, datum, metric_module_id, cell_name, new_cell_value):
        try:
            # updating changed value by new value
            response = api.get_metric_module(request, metric_module_id)
            data = json.loads(response.text)
            # TODO: Check only the valid keys, delete the rest
            if 'id' in data:  # PUT does not allow this key
                del data['id']
            if 'path' in data:  # PUT does not allow this key
                del data['path']

            data[cell_name] = new_cell_value
            api.update_metric_module_metadata(request, metric_module_id, data)
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

    def get_data(self, request, metric_module_id):
        response = api.get_metric_module(request, metric_module_id)
        data = json.loads(response.text)

        filter = MetricModule(data['id'], data['metric_name'], data['class_name'], data['put'],
                              data['get'], data['replicate'], data['execution_server'], data['status'])
        return filter


class MetricTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    metric_name = tables.Column('metric_name', verbose_name=_("Metric Name"))
    class_name = tables.Column('class_name', verbose_name=_("Class Name"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    methods = tables.Column('methods', verbose_name=_("HTTP Methods"), form_field=forms.CharField(max_length=255))
    execution_server = tables.Column('execution_server', verbose_name=_("Execution Server"),
                                     form_field=forms.ChoiceField(choices=[('proxy', _('Proxy Node')), ('object', _('Storage Node')), ('proxy/object', _('Proxy & Storage Nodes'))]),
                                     update_action=UpdateCell)
    status = tables.Column('status', verbose_name=_("Status"))

    class Meta:
        name = "metric_modules"
        verbose_name = _("Metric Modules")
        table_actions_menu = (EnableMultipleMetricModules, DisableMultipleMetricModules,)  # dropdown menu
        table_actions = (MyFilterAction, UploadMetricModule, DeleteMultipleMetricModules,)
        row_actions = (EnableMetricModule, DisableMetricModule, UpdateMetricModule, DownloadMetricModule, DeleteMetricModule,)
        row_class = UpdateRow
