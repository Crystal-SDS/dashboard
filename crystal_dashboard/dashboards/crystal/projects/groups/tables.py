from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from horizon import tables


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateGroup(tables.LinkAction):
    name = "create_group"
    verbose_name = _("Create Group")
    url = "horizon:crystal:projects:groups:create"
    classes = ("ajax-modal",)
    icon = "plus"


class GroupsTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    tenants = tables.Column('projects', verbose_name=_("Projects"))

    class Meta:
        name = "groups"
        verbose_name = _("Groups")
        table_actions = (MyFilterAction, CreateGroup)
