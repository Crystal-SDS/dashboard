from django.utils.translation import ugettext_lazy as _
from horizon import tables


class MetricTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("Name"))
    network_location = tables.Column('network_location', verbose_name="Network Location")
    type = tables.Column('type', verbose_name=_("Type"))

    class Meta:
        name = "workload_metrics"
        verbose_name = _("Workload Metrics")
