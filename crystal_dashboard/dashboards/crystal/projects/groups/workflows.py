from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from horizon import exceptions
from horizon import messages
from horizon import tables
from horizon.utils import memoized
from horizon import views
from horizon import workflows
from horizon import forms
   

class CreateGroupInfoAction(workflows.Action):
    

    name = forms.CharField(label=_("Name"),
                           max_length=64)

    def __init__(self, request, *args, **kwargs):
        super(CreateGroupInfoAction, self).__init__(request,
                                                      *args,
                                                      **kwargs)

    class Meta(object):
        name = _("Group Information")
        help_text = _("Create a group")
    
    
class CreateGroupInfo(workflows.Step):
    action_class = CreateGroupInfoAction

    contributes = ("name",)

    def __init__(self, workflow):
        super(CreateGroupInfo, self).__init__(workflow)            


class GroupMembersAction(workflows.MembershipAction):
    def __init__(self, request, *args, **kwargs):
        super(GroupMembersAction, self).__init__(request,
                                                         *args,
                                                         **kwargs)
        err_msg = _('Unable to retrieve projects list. Please try again later.')
        # Use the domain_id from the project

        if 'project_id' in self.initial:
            project_id = self.initial['project_id']

        default_role_name = self.get_default_role_field_name()
        self.fields[default_role_name] = forms.CharField(required=False)
        self.fields[default_role_name].initial = 0
        
        # Get list of available users
        all_users = []
        try:
            pass
        except Exception:
            exceptions.handle(request, err_msg)
        users_list = [(user.id, user.name) for user in all_users]
        users_list = [('1', 'A'), ('2', 'B'), ('3', 'C')]
        role_list = [('1', 'A'), ('2', 'B')]
        
        for role in role_list:
            field_name = self.get_member_field_name(role[0])
            label = role[1]
            self.fields[field_name] = forms.MultipleChoiceField(required=False,
                                                                label=label)
            self.fields[field_name].choices = users_list
            self.fields[field_name].initial = []
        
        print self.fields

    class Meta(object):
        name = _("Group projects")
        slug = 'group_projects'
        

class GroupMembers(workflows.UpdateMembersStep):

    action_class = GroupMembersAction
    show_roles = False

    def contribute(self, data, context):
        return context
    
    
class CreateGroup(workflows.Workflow):
    slug = "create_group"
    name = _("Create Group")
    finalize_button_name = _("Create Group")
    success_message = _('Created new group "%s".')
    failure_message = _('Unable to create group "%s".')
    success_url = "horizon:crystal:projects:index"
    default_steps = (CreateGroupInfo,
                     GroupMembers,)

    def __init__(self, request=None, context_seed=None, entry_point=None,
                 *args, **kwargs):
        
        super(CreateGroup, self).__init__(request=request,
                                            context_seed=context_seed,
                                            entry_point=entry_point,
                                            *args,
                                            **kwargs)


    def handle(self, request, data):
        return True