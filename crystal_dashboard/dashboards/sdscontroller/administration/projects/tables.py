# from django.core.urlresolvers import reverse
# from django.utils.translation import ugettext_lazy as _
# from django.utils.translation import ungettext_lazy
#
# from horizon import exceptions
# from horizon import messages
# from horizon import tables
# from openstack_dashboard.api import sds_controller as api
# from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception
#
#
# class MyFilterAction(tables.FilterAction):
#     name = "myfilter"
#
#
# class CreateGroup(tables.BatchAction):
#     @staticmethod
#     def action_present(count):
#         return ungettext_lazy(
#             u"Create Group",
#             u"Create Group",
#             count
#         )
#
#     @staticmethod
#     def action_past(count):
#         return ungettext_lazy(
#             u"Create Group",
#             u"Create Group",
#             count
#         )
#
#     name = "createGroup"
#     icon = "plus"
#     success_url = "horizon:sdscontroller:administration:index"
#
#     def handle(self, data_table, request, obj_ids):
#         try:
#             response = api.dsl_create_tenants_group(request, None, obj_ids)
#             if 200 <= response.status_code < 300:
#                 messages.success(request, _('Successfully created group.'))
#             else:
#                 raise sdsexception.SdsException(response.text)
#         except Exception as ex:
#             redirect = reverse("horizon:sdscontroller:administration:index")
#             error_message = "Unable to create group.\t %s" % ex.message
#             exceptions.handle(request, _(error_message), redirect=redirect)
#
#
# class ProjectTable(tables.DataTable):
#     id = tables.Column('id', verbose_name=_("ID"))
#     name = tables.Column('name', verbose_name=_("Name"))
#     description = tables.Column('description', verbose_name=_("Description"))
#     enabled = tables.Column('enabled', verbose_name=_("Enabled"))
#
#     class Meta:
#         name = "projects"
#         verbose_name = _("Projects")
#         table_actions = (MyFilterAction, CreateGroup,)
