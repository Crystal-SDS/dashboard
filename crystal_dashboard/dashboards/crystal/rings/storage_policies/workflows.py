from django.utils.translation import ugettext_lazy as _

from horizon import forms
from horizon import workflows
from horizon import exceptions
from django.core.urlresolvers import reverse
import json
from crystal_dashboard.api import swift as api
from crystal_dashboard.dashboards.crystal.nodes import models as nodes_models



INDEX_URL = "horizon:crystal:rings:index"

class StoragePolicyInfoAction(workflows.Action):
    
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the new policy."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))
    
    policy_id = forms.CharField(max_length=5,
                                label=_("Policy ID"),
                                help_text=_("The unique ID to identify the policy."),
                                widget=forms.TextInput(
                                    attrs={"ng-model": "policy_id", "not-blank": ""}
                                ), 
                                required=False)

    replicas = forms.CharField(max_length=255,
                               label=_("Num. Replicas"),
                               required=False,
                               help_text=_("Number of replicas"),
                               widget=forms.TextInput(
                                   attrs={"ng-model": "replicas", "not-blank": ""}
                               ))

    partitions = forms.CharField(max_length=255,
                                 label=_("Num. Partitions"),
                                 required=False,
                                 help_text=_("If the value is x the num of partitions will be 2^x"),
                                 widget=forms.TextInput(
                                     attrs={"ng-model": "partitions", "not-blank": ""}
                                 ))

    time = forms.CharField(max_length=255,
                           label=_("Time"),
                           required=False,
                           help_text=_("Time between moving a partition more than once. In hours"),
                           widget=forms.TextInput(
                               attrs={"ng-model": "time", "not-blank": ""}
                           ))


    class Meta(object):
        name = _("Storage policy information")
        help_text = _("Create a storage policy")


class StoragePolicyInfo(workflows.Step):
    action_class = StoragePolicyInfoAction
    
    contributes = ("name", "storage_node", "replicas", "partitions", "time",)
    
    def contribute(self, data, context):          
        context.update(data)
        return context


class UpdateProjectMembersAction(workflows.MembershipAction):
    def __init__(self, request, *args, **kwargs):
        super(UpdateProjectMembersAction, self).__init__(request,
                                                         *args,
                                                         **kwargs)
        
        err_msg = _('Unable to retrieve nodes list. Please try again later.')
        
        self.fields['testing'] = forms.CharField(required=False)
        self.fields['testing'].initial = 5
        
        try:
            self.response = api.swift_get_all_nodes(self.request)
            
            if 200 <= self.response.status_code < 300:
                strobj = self.response.text
            else:
                error_message = 'Unable to get nodes.'
                raise sdsexception.SdsException(error_message)
            
        except Exception as e:
            strobj = '[]'
            exceptions.handle(self.request, e.message)

        nodes = json.loads(strobj)
                
        field_name = self.get_member_field_name('nodes')
        self.fields[field_name] = forms.MultipleChoiceField(required=False,
                                                                label='nodes')
        self.fields[field_name].choices = [(ind, node['name']) for ind, node in enumerate(nodes)]
        self.fields[field_name].initial = [] 
            
    class Meta(object):
        name = _("Nodes")
        slug = "projectmembers"


class UpdateProjectMembers(workflows.UpdateMembersStep):
    action_class = UpdateProjectMembersAction
    available_list_title = _("All Nodes")
    members_list_title = _("Nodes selected")
    no_available_text = _("No nodes found.")
    no_members_text = _("No nodes selected.")

    def contribute(self, data, context):
        return context


class CreateStoragePolicyClass(workflows.Workflow):
    default_steps = (StoragePolicyInfo, UpdateProjectMembers,)
    name = "Create Storage Policy"
    slug = "CreateStoragePolicy"
    submit_label = _("Create Storage Policy")
    success_url = 'horizon:crystal:rings:index'

    def handle(self, request, data):
        return data

        # TODO: After rebuild the form this code should disappear
#         try:
#             storage_nodes_response = api.list_storage_nodes(request)
#             if storage_nodes_response.text:
#                 storage_nodes = json.loads(storage_nodes_response.text)
#                 storage_nodes_form = data['storage_node'].split(',')
#                 data["storage_node"] = {}
#                 for i in range(0, len(storage_nodes_form), 2):
#                     for storage_node in storage_nodes:
#                         if storage_node["id"] == storage_nodes_form[i]:
#                             location = storage_node['location']
#                             data["storage_node"][location] = storage_nodes_form[i + 1]
#             else:
#                 raise Exception
#         except Exception, e:
#             redirect = reverse("horizon:crystal:rings_and_accounts:index")
#             error_message = "Storage nodes not found"
#             exceptions.handle(request,
#                               _(error_message),
#                               redirect=redirect)
#         try:
#             response = api.new_storage_policy(request, data)
#             if 200 <= response.status_code < 300:
#                 messages.success(request, _('Successfully EC Storage Policy created.'))
#                 return data
#             else:
#                 raise sdsexception.SdsException(response.text)
#         except Exception as ex:
#             redirect = reverse("horizon:crystal:rings_and_accounts:index")
#             error_message = "Unable to EC Storage Policy.\t %s" % ex.message
#             exceptions.handle(request,
#                               _(error_message),
#                               redirect=redirect)