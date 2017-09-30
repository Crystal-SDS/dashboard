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


class CreateZone(tables.LinkAction):
    name = "create_zone"
    verbose_name = _("Create Zone")
    url = "horizon:crystal:zones:create"
    classes = ("ajax-modal",)
    icon = "plus"


class UpdateZoneAction(tables.LinkAction):
    name = "update_zone"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, datum=None):
        base_url = reverse("horizon:crystal:zones:update", kwargs={'zone_id': datum.id})
        return base_url


class DeleteZoneAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Zone",
            u"Delete Zones",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Zone deleted",
            u"Zones deleted",
            count
        )

    name = "delete"
    success_url = "horizon:crystal:zones:index"

    def delete(self, request, zone_id):
        try:
            response = api.delete_zone(request, zone_id)
            if not 200 <= response.status_code < 300:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:zones:index")
            error_message = "Unable to delete zone.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)


class ZonesTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    region = tables.Column('region', verbose_name=_("Region"))
    description = tables.Column('description', verbose_name=_("Description"))

    class Meta:
        name = "zones"
        verbose_name = _("Zones")
        table_actions = (CreateZone, MyFilterAction,)
        row_actions = (UpdateZoneAction, DeleteZoneAction,)
