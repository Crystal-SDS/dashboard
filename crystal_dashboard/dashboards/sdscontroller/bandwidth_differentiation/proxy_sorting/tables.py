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
from models import ProxySorting
from crystal_dashboard.api import crystal as api
from crystal_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateSortedMethod(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Sorted Method")
    url = "horizon:sdscontroller:bandwidth_differentiation:proxy_sorting:upload"
    classes = ("ajax-modal",)
    icon = "plus"


class UpdateSortedMethod(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, proxy_sorting):
        base_url = reverse("horizon:sdscontroller:bandwidth_differentiation:proxy_sorting:update", kwargs={'proxy_sorting_id': proxy_sorting.id})
        return base_url


class UpdateCell(tables.UpdateAction):
    def allowed(self, request, project, cell):
        return cell.column.name == 'criterion'

    def update_cell(self, request, datum, id, cell_name, new_cell_value):
        try:
            # updating changed value by new value
            response = api.bw_get_sort_method(request, id)
            data = json.loads(response.text)
            data[cell_name] = new_cell_value
            api.bw_update_sort_method(request, id, data)
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
        response = api.bw_get_sort_method(request, id)
        data = json.loads(response.text)

        proxy_sorting = ProxySorting(data['id'], data['name'], data['criterion'])
        return proxy_sorting


class DeleteSortedMethod(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Sorted Method",
            u"Delete Sorted Methods",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Sorted Method",
            u"Deleted Sorted Methods",
            count
        )

    name = "delete_proxy_sorting"
    success_url = "horizon:sdscontroller:bandwidth_differentiation:index"

    def delete(self, request, obj_id):
        try:
            response = api.bw_delete_sort_method(request, obj_id)
            if 200 <= response.status_code < 300:
                pass
                # messages.success(request, _('Successfully deleted sorted method: %s') % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to remove sorted method.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class DeleteMultipleSortedMethods(DeleteSortedMethod):
    name = "delete_multiple_proxy_sorting"


class ProxySortingTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    criterion = tables.Column('criterion', verbose_name=_("Criterion"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)

    class Meta:
        name = "proxy_sorting"
        verbose_name = _("Proxy Sorting")
        table_actions = (MyFilterAction, CreateSortedMethod, DeleteMultipleSortedMethods,)
        row_actions = (UpdateSortedMethod, DeleteSortedMethod,)
        row_class = UpdateRow
