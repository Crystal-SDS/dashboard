from django.utils.translation import ugettext_lazy as _
import horizon


class SwiftCluster(horizon.PanelGroup):
    slug = "swift_cluster"
    name = _("Swift Cluster")
    panels = ('regions', 'zones', 'nodes', 'rings', 'containers',)


class SDSManagement(horizon.PanelGroup):
    name = _("SDS Management")
    slug = "sds_management"
    panels = ('projects', 'filters', 'metrics', 'policies', 'controllers', 'analytics_jobs')


class Monitoring(horizon.PanelGroup):
    name = _("Monitoring")
    slug = "monitoring"
    panels = ('swift_monitoring', 'kibana', 'analytics_monitoring')


class CrystalController(horizon.Dashboard):
    name = _("Crystal Controller")
    slug = "crystal"
    panels = (SwiftCluster, SDSManagement, Monitoring,)  # Add your panels here.
    default_panel = 'projects'  # Specify the slug of the default panel.
    permissions = ('openstack.roles.admin', 'openstack.services.object-store', )


horizon.register(CrystalController)
