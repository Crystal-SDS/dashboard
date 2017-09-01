from django.utils.translation import ugettext_lazy as _
import horizon


class SwiftCluster(horizon.PanelGroup):
    slug = "swift_cluster"
    name = _("Swift Cluster")
    panels = ('nodes', 'rings', 'containers',)


class SDSManagement(horizon.PanelGroup):
    slug = "sds_management"
    name = _("SDS Management")
    panels = ('projects', 'filters', 'workload_metrics', 'sds_policies', 'bandwidth_differentiation',)


class Monitoring(horizon.PanelGroup):
    slug = "monitoring"
    name = _("Monitoring")
    panels = ('swift_monitoring', 'kibana',)


class CrystalController(horizon.Dashboard):
    name = _("Crystal Controller")
    slug = "sdscontroller"
    panels = (SwiftCluster, SDSManagement, Monitoring,)  # Add your panels here.
    default_panel = 'sds_policies'  # Specify the slug of the default panel.
    permissions = ('openstack.roles.admin', 'openstack.services.object-store',)


horizon.register(CrystalController)
