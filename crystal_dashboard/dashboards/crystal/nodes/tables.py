import calendar
import collections
import time

from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import register  # noqa
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables
from horizon import exceptions
from crystal_dashboard.api import swift as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class MyProxyFilterAction(tables.FilterAction):
    name = "myproxyfilter"


class UpdateProxyAction(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, datum=None):
        base_url = reverse("horizon:crystal:nodes:update", kwargs={'node_id': datum.id,
                                                                   'server': 'proxy'})
        return base_url


class RestartProxyAction(tables.BatchAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Restart Swift Proxy Node",
            u"Restart Swift Proxy Nodes",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Swift Proxy Node Restarted",
            u"Swift Proxy Nodes Restarted",
            count
        )

    name = "restart"
    verbose_name = _("Restart Swift")
    success_url = "horizon:crystal:nodes:index"

    def action(self, request, node_id):
        response = api.swift_restart_node(request, 'proxy', node_id)
        if 200 <= response.status_code < 300:
            pass
        else:
            exceptions.handle(request)

class RestartMultipleProxyNodes(RestartProxyAction):
    name = "restart_multiple_proxy_nodes"

class DeleteProxyNodeAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Node",
            u"Delete Nodes",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Node deleted",
            u"Nodes deleted",
            count
        )

    name = "delete"
    success_url = "horizon:crystal:nodes:index"

    def delete(self, request, node_id):
        try:
            response = api.swift_delete_node(request, 'proxy', node_id)
            if 200 <= response.status_code < 300:
                pass
                # messages.success(request, _('Successfully deleted node: %s') % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:nodes:index")
            error_message = "Unable to delete node.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)


class ProxysTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("Hostname"))
    ip = tables.Column('ip', verbose_name="IP")
    region_id = tables.Column('region_id', verbose_name="Region")
    zone_id = tables.Column('zone_id', verbose_name="Zone")
    ssh_access = tables.Column('ssh_access', verbose_name="SSH Access")
    last_ping = tables.Column(lambda obj: '{0} seconds ago'.format(calendar.timegm(time.gmtime()) - int(float(getattr(obj, 'last_ping', '0')))),
                              verbose_name="Last Swift ping")
    node_status = tables.Column(lambda obj: 'UP' if getattr(obj, 'node_status', False) is True else 'DOWN', verbose_name="Swift Status", status=True)

    class Meta:
        name = "proxys"
        verbose_name = _("Proxys")
        table_actions = (MyProxyFilterAction, RestartMultipleProxyNodes,)
        row_actions = (UpdateProxyAction, RestartProxyAction, DeleteProxyNodeAction)
        hidden_title = False


@register.filter
def usage_percentage(free, size):
    try:
        usage = float(size - free) * 100 / size
        return "{0:.2f}%".format(usage)
    except (ValueError, ZeroDivisionError):
        return None


def get_devices_info(storage_node):
    template_name = 'crystal/nodes/_devices_info.html'
    ordered_devices = collections.OrderedDict(sorted(storage_node.devices.items()))
    context = {"devices": ordered_devices}
    return template.loader.render_to_string(template_name, context)


class MyStorageNodeFilterAction(tables.FilterAction):
    name = "mystoragenodefilter"


class UpdateStorageNodeAction(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, datum=None):
        base_url = reverse("horizon:crystal:nodes:update", kwargs={'node_id': datum.id,
                                                                   'server': 'object'})
        return base_url


class RestartStorageNodeAction(tables.BatchAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Restart Swift Storage Node",
            u"Restart Swift Storage Nodes",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Swift Storage Node Restarted",
            u"Swift Storage Nodes Restarted",
            count
        )

    name = "restart"
    verbose_name = _("Restart Swift")
    success_url = "horizon:crystal:nodes:index"

    def action(self, request, node_id):
        response = api.swift_restart_node(request, 'object', node_id)
        if 200 <= response.status_code < 300:
            pass
        else:
            exceptions.handle(request)


class RestartMultipleStorageNodes(RestartStorageNodeAction):
    name = "restart_multiple_storage_nodes"


class DeleteStorageNodeAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Node",
            u"Delete Nodes",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Node deleted",
            u"Nodes deleted",
            count
        )

    name = "delete"
    success_url = "horizon:crystal:nodes:index"

    def delete(self, request, node_id):
        try:
            response = api.swift_delete_node(request, 'object', node_id)
            if 200 <= response.status_code < 300:
                pass
                # messages.success(request, _('Successfully deleted node: %s') % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:nodes:index")
            error_message = "Unable to delete node.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)


class StorageNodesTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("Hostname"))
    ip = tables.Column('ip', verbose_name="IP")
    region_id = tables.Column('region_id', verbose_name="Region")
    zone_id = tables.Column('zone_id', verbose_name="Zone")
    ssh_access = tables.Column('ssh_access', verbose_name="SSH Access")
    last_ping = tables.Column(lambda obj: '{0} seconds ago'.format(calendar.timegm(time.gmtime()) - int(float(getattr(obj, 'last_ping', '0')))),
                              verbose_name="Last Swift ping")
    node_status = tables.Column(lambda obj: 'UP' if getattr(obj, 'node_status', False) is True else 'DOWN', verbose_name="Swift Status", status=True)

    devices = tables.Column(get_devices_info, verbose_name=_("Devices"), classes=('nowrap-col',), sortable=False)

    class Meta:
        name = "storagenodes"
        verbose_name = _("Storage Nodes")
        table_actions = (MyStorageNodeFilterAction, RestartMultipleStorageNodes)
        row_actions = (UpdateStorageNodeAction, RestartStorageNodeAction, DeleteStorageNodeAction)
        hidden_title = False
