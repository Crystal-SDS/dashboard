# from django.utils.translation import ugettext_lazy as _
#
# from openstack_dashboard.dashboards.sdscontroller.storagepolicies.dynamic_policies.tables import PoliciesTable as tables
#
#
# class MyFilterAction(tables.FilterAction):
#     name = "myfilter"
#
#
# class InstancesTable(tables):
#     id = tables.Column('id', verbose_name=_("ID"))
#     policy = tables.Column('policy', verbose_name=_("Policy"))
#
#     class Meta:
#         name = "instances"
#         verbose_name = _("Instances")
#         table_actions = (MyFilterAction,)
