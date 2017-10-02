from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from horizon import exceptions
from horizon import messages
from horizon import tables


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateStoragePolicy(tables.LinkAction):
    name = "create_storage_policy"
    verbose_name = _("Create Replication Policy")
    url = "horizon:crystal:rings:storage_policies:create_storage_policy"
    classes = ("ajax-modal",)
    icon = "plus"


class CreateECStoragePolicy(tables.LinkAction):
    name = "create_ec_storage_policy"
    verbose_name = _("Create EC Policy")
    url = "horizon:crystal:rings:storage_policies:create_ec_storage_policy"
    classes = ("ajax-modal",)
    icon = "plus"


class LoadSwiftPolicies(tables.LinkAction):
    name = "load_swift_policies"
    verbose_name = _("Load Swift Policies")
    url = "horizon:crystal:rings:storage_policies:load_swift_policies"
    classes = ("ajax-modal",)
    icon = "plus"


class StoragePolicyTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    type = tables.Column('type', verbose_name=_("Type"))

    class Meta:
        name = "storagepolicies"
        verbose_name = _("Storage Policies")
        table_actions = (MyFilterAction, CreateStoragePolicy, CreateECStoragePolicy, LoadSwiftPolicies,)
