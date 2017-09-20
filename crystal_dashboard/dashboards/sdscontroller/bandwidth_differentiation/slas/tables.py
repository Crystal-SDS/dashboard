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
from models import SLA
from crystal_dashboard.api import sds_controller as api
from crystal_dashboard.dashboards.sdscontroller import common
from crystal_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateSLA(tables.LinkAction):
    name = "create"
    verbose_name = _("Create SLO")
    url = "horizon:sdscontroller:bandwidth_differentiation:slas:create_sla"
    classes = ("ajax-modal",)
    icon = "plus"


class UpdateSLA(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, datum=None):
        base_url = reverse("horizon:sdscontroller:bandwidth_differentiation:slas:update_sla", kwargs={"sla_id": datum.id})
        return base_url


class UpdateCell(tables.UpdateAction):
    def allowed(self, request, project, cell):
        return cell.column.name in ["get_bandwidth", "put_bandwidth", "ssync_bandwidth"]

    def update_cell(self, request, datum, id, cell_name, new_cell_value):
        try:
            # updating changed value by new value
            #response = api.bw_get_sla(request, id)
            #response = api.bw_get_sla(request, "bandwidth", cell_name, id)
            #data = json.loads(response.text)
            #data[cell_name] = new_cell_value

            slo_names_dict = {'get_bandwidth': 'get_bw', 'put_bandwidth': 'put_bw', 'ssync_bandwidth': 'ssync_bw'}
            api.fil_update_slo(request, 'bandwidth', slo_names_dict[cell_name], id, {'value': new_cell_value})
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
        get_sla = api.fil_get_slo(request, 'bandwidth', 'get_bw', id)
        put_sla = api.fil_get_slo(request, 'bandwidth', 'put_bw', id)
        ssync_sla = api.fil_get_slo(request, 'bandwidth', 'ssync_bw', id)

        get_sla_json = json.loads(get_sla.text)
        put_sla_json = json.loads(put_sla.text)
        ssync_sla_json = json.loads(ssync_sla.text)

        storage_policies_dict = dict(common.get_storage_policy_list(request, common.ListOptions.by_id()))
        projects_dict = dict(common.get_project_list(request))

        project_target, policy_id = get_sla_json['target'].split('#')  # target format is AUTH_X#Y where  X is the project_id and Y is the policy_id
        project_id = project_target.split('_')[1]

        sla = SLA(project_id, projects_dict[str(project_id)], policy_id, storage_policies_dict[str(policy_id)], get_sla_json['value'],
                  put_sla_json['value'], ssync_sla_json['value'])
        return sla


        # response = api.bw_get_sla(request, id)
        # data = json.loads(response.text)
        #
        # sla = SLA(data["project_id"], data["project_name"], data["policy_id"], data["policy_name"], data["bandwidth"])
        # return sla


class DeleteSLA(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete SLO",
            u"Delete SLOs",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted SLO",
            u"Deleted SLOs",
            count
        )

    name = "delete_sla"
    success_url = "horizon:sdscontroller:bandwidth_differentiation:index"

    def delete(self, request, obj_id):
        try:
            #response = api.bw_delete_sla(request, obj_id)
            success = True
            error_msg = ''
            for slo_name in ['get_bw', 'put_bw', 'ssync_bw']:
                response = api.fil_delete_slo(request, 'bandwidth', slo_name, obj_id)
                if 200 <= response.status_code < 300:
                    pass
                    # messages.success(request, _("Successfully deleted sla: %s") % obj_id)
                else:
                    success = False
                    error_msg = response.text
            if not success:
                raise sdsexception.SdsException(error_msg)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to remove sla.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class DeleteMultipleSLAs(DeleteSLA):
    name = "delete_multiple_slas"


class SLAsTable(tables.DataTable):
    tenant_name = tables.Column("project_name", verbose_name=_("Project Name"))
    tenant_id = tables.Column("project_id", verbose_name=_("Project ID"))
    policy_name = tables.Column("policy_name", verbose_name=_("Storage Policy (Ring)"))
    get_bandwidth = tables.Column("get_bw", verbose_name=_("GET BW"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    put_bandwidth = tables.Column("put_bw", verbose_name=_("PUT BW"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    ssync_bandwidth = tables.Column("ssync_bw", verbose_name=_("SSYNC BW"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)

    class Meta:
        name = "slas"
        verbose_name = _("SLOs")
        table_actions = (MyFilterAction, CreateSLA, DeleteMultipleSLAs,)
        row_actions = (UpdateSLA, DeleteSLA,)
        row_class = UpdateRow