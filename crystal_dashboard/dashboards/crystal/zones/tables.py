from django.utils.translation import ugettext_lazy as _
from horizon import tables


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateZone(tables.LinkAction):
    name = "create_zone"
    verbose_name = _("Create new zone")
    url = "horizon:crystal:zones:create_zone"
    classes = ("ajax-modal",)
    icon = "plus"


class StoragePolicyTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    description = tables.Column('description', verbose_name=_("Description"))

    class Meta:
        name = "zones"
        verbose_name = _("Zones")
        table_actions = (CreateZone, MyFilterAction,)
