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
from models import Filter
from crystal_dashboard.api import crystal as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateFilter(tables.LinkAction):
    name = "create"
    verbose_name = _("Register Filter")
    url = "horizon:crystal:filters:registry_dsl:create_filter"
    classes = ("ajax-modal",)
    icon = "plus"


class UpdateFilter(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, datum=None):
        base_url = reverse("horizon:crystal:filters:registry_dsl:update_filter", kwargs={'name': datum.name})
        return base_url


class DeleteDslFilter(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Filter",
            u"Delete Filters",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Filter",
            u"Deleted Filters",
            count
        )

    name = "delete_filter"
    success_url = "horizon:crystal:filters:index"

    def delete(self, request, obj_id):
        try:
            datum = self.table.get_object_by_id(obj_id)
            obj_name = datum.name
            response = api.dsl_delete_filter(request, obj_name)
            if 200 <= response.status_code < 300:
                pass
                # messages.success(request, _('Successfully deleted filter: %s') % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:filters:index")
            error_message = "Unable to remove filter.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdateCell(tables.UpdateAction):
    def allowed(self, request, project, cell):
        return ((cell.column.name == 'activation_url') or
                (cell.column.name == 'valid_parameters'))

    def update_cell(self, request, datum, name,
                    cell_name, new_cell_value):
        # inline update project info
        try:
            # updating changed value by new value
            response = api.dsl_get_filter_metadata(request, name)
            data = json.loads(response.text)
            data[cell_name] = new_cell_value
            api.dsl_update_filter(request, name, data)
        except Conflict:
            # Returning a nice error message about name conflict. The message
            # from exception is not that clear for the user
            message = _("This name is already taken.")
            raise ValidationError(message)
        except Exception:
            exceptions.handle(request, ignore=True)
            return False
        return True


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, name):
        response = api.dsl_get_filter_metadata(request, name)
        data = json.loads(response.text)
        filter_dsl = Filter(data['identifier'], name, data['activation_url'], data['valid_parameters'], 'filter name')
        return filter_dsl


class DeleteMultipleDslFilters(DeleteDslFilter):
    name = "delete_multiple_filters"


class DslFilterTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_("Name"))
    filter_identifier = tables.Column('filter_identifier_name', verbose_name=_("Filter"))
    activation_url = tables.Column('activation_url', verbose_name=_("API Activation Url"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    valid_parameters = tables.Column('valid_parameters', verbose_name=_("Valid Parameters"), form_field=forms.CharField(max_length=64), update_action=UpdateCell)

    def __init__(self, request, data=None, needs_form_wrapper=None, **kwargs):
        super(DslFilterTable, self).__init__(request, data=data, needs_form_wrapper=needs_form_wrapper, **kwargs)

    class Meta:
        name = "dsl_filters"
        verbose_name = _("Filters")
        row_class = UpdateRow
        table_actions = (MyFilterAction, CreateFilter, DeleteMultipleDslFilters,)
        row_actions = (UpdateFilter, DeleteDslFilter,)
