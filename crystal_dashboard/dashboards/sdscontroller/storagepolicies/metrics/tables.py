from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from django.core.urlresolvers import reverse

from horizon import tables
from horizon import exceptions
from horizon import messages

from openstack_dashboard.api import sds_controller as api


# class CreatePolicy(tables.LinkAction):
#     name = "create"
#     verbose_name = _("Create Policy")
#     url = "horizon:sdscontroller:storagepolicies:dynamic_policies:create_policy"
#     classes = ("ajax-modal",)
#     icon = "plus"
#
#
# class DeletePolicy(tables.DeleteAction):
#     @staticmethod
#     def action_present(count):
#         return ungettext_lazy(
#             u"Delete Policy",
#             u"Delete Policies",
#             count
#         )
#
#     @staticmethod
#     def action_past(count):
#         return ungettext_lazy(
#             u"Deleted Policy",
#             u"Deleted Policies",
#             count
#         )
#
#     name = "delete_policy"
#     success_url = "horizon:sdscontroller:storagepolicies:index"
#
#     def delete(self, request, obj_id):
#         try:
#             response = api.remove_policy(obj_id)
#             if 200 <= response.status_code < 300:
#                 messages.success(request, _('Successfully deleted policy/rule: %s') % obj_id)
#             else:
#                 raise ValueError(response.text)
#         except Exception as ex:
#             redirect = reverse("horizon:sdscontroller:storagepolicies:index")
#             error_message = "Unable to remove policy.\t %s" % ex.message
#             exceptions.handle(request,
#                               _(error_message),
#                               redirect=redirect)


# class DeleteMultiplePolicies(DeletePolicy):
#     name = "delete_multiple_policies"


class MetricTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("Name"))
    network_location = tables.Column('network_location', verbose_name="Network Location")
    type = tables.Column('type', verbose_name=_("Type"))

    class Meta:
        name = "workload_metrics"
        verbose_name = _("Workload Metrics")
        # table_actions = (CreatePolicy, DeleteMultiplePolicies,)
        # table_actions = (CreatePolicy,)
        # row_actions = (DeletePolicy,)
