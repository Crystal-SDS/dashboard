from django.utils.translation import ugettext_lazy as _
from horizon import tables
from django.core.urlresolvers import reverse
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from horizon import exceptions
from crystal_dashboard.api import swift as api


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateRegion(tables.LinkAction):
    name = "create_region"
    verbose_name = _("Create Region")
    url = "horizon:crystal:regions:create"
    classes = ("ajax-modal",)
    icon = "plus"


class UpdateRegionAction(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, datum=None):
        base_url = reverse("horizon:crystal:regions:update", kwargs={'region_id': datum.id})
        return base_url


class DeleteRegionAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Region",
            u"Delete Regions",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Region deleted",
            u"Regions deleted",
            count
        )

    name = "delete"
    success_url = "horizon:crystal:regions:index"

    def delete(self, request, region_id):
        try:
            response = api.delete_region(request, region_id)
            if not 200 <= response.status_code < 300:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:regions:index")
            error_message = "Unable to delete region.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)


class RegionsTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    description = tables.Column('description', verbose_name=_("Description"))

    class Meta:
        name = "regions"
        verbose_name = _("Regions")
        table_actions = (CreateRegion, MyFilterAction,)
        row_actions = (UpdateRegionAction, DeleteRegionAction,)
