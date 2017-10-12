from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from horizon import exceptions
from horizon import messages
from horizon import tables
from horizon.utils import memoized
from horizon import views
from horizon import workflows
from horizon import forms
from crystal_dashboard.dashboards.crystal import common


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
        super(GroupMembersAction, self).__init__(request, *args, **kwargs)
        err_msg = _('Unable to retrieve projects list. Please try again later.')

        default_role_field_name = self.get_default_role_field_name()
        self.fields[default_role_field_name] = forms.CharField(required=True)
        self.fields[default_role_field_name].initial = 'member'

        field_name = self.get_member_field_name('member')
        self.fields[field_name] = forms.MultipleChoiceField(required=True)

        # Fetch the projects crytsal-enabled list and add to policy options
        projects_crystal_enabled = []
        try:
            projects_crystal_enabled = common.get_project_list_crystal_enabled(request)
        except Exception:
            exceptions.handle(request, err_msg)

        self.fields[field_name].choices = projects_crystal_enabled

    class Meta(object):
        name = _("Group projects")
        slug = 'group_projects'


class GroupMembers(workflows.UpdateMembersStep):

    action_class = GroupMembersAction
    show_roles = False
    contributes = ("attached_projects",)

    def contribute(self, data, context):
        if data:
            member_field_name = self.get_member_field_name('member')
            context['attached_projects'] = data.get(member_field_name, [])
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
        print data
        return True
