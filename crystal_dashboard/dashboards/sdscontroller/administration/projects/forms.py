# from django.core.urlresolvers import reverse
# from django.utils.translation import ugettext_lazy as _
#
# from horizon import exceptions
# from horizon import forms
# from horizon import messages
# from openstack_dashboard.api import sds_controller as api
# from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception
#
#
# # TODO in construction
# class CreateGroup(forms.SelfHandlingForm):
#     name = forms.CharField(max_length=255,
#                            label=_("Name"),
#                            help_text=_("The name of the group to be created."),
#                            required=True,
#                            widget=forms.TextInput(
#                                attrs={"ng-model": "name", "not-blank": ""}
#                            ))
#
#     projects_ids = forms.CharField(max_length=255,
#                                    label=_("Project Id List"),
#                                    help_text=_("A comma spared list with project ids."),
#                                    required=True,
#                                    widget=forms.TextInput(
#                                        attrs={"ng-model": "project_ids", "not-blank": ""}
#                                    ))
#
#     @staticmethod
#     def handle(request, data):
#         name = data["name"]
#         project_ids = data["project_ids"]
#
#         try:
#             response = api.dsl_create_tenants_group(request, name, project_ids)
#             if 200 <= response.status_code < 300:
#                 messages.success(request, _('Successfully created group: %s') % data['name'])
#                 return data
#             else:
#                 raise sdsexception.SdsException(response.text)
#         except Exception as ex:
#             redirect = reverse("horizon:sdscontroller:administration:index")
#             error_message = "Unable to create group.\t %s" % ex.message
#             exceptions.handle(request, _(error_message), redirect=redirect)
