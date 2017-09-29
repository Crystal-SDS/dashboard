from django.utils.translation import ugettext_lazy as _
from horizon import tables


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class GroupsTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    tenants = tables.Column('projects', verbose_name=_("Projects"))

    class Meta:
        name = "groups"
        verbose_name = _("Groups")
        table_actions = (MyFilterAction,)
