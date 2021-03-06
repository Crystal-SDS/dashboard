from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from crystal_dashboard.api import policies as api
from crystal_dashboard.dashboards.crystal import common
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from openstack_dashboard import api as api_keystone


class CreateAccessControlPolicy(forms.SelfHandlingForm):

    project_choices = []
    project_id = forms.ChoiceField(choices=project_choices,
                                   label=_("Project"),
                                   help_text=_("The project where the rule will be applied."),
                                   required=True)

    container_choices = [('', 'None')]
    container_id = forms.CharField(label=_("Container"),
                                   help_text=_("The container where the rule will be applied."),
                                   required=False,
                                   widget=forms.Select(choices=container_choices))

    users_choices = [('', 'None')]
    identity = forms.CharField(label=_("User/Group"),
                               help_text=_("The user or group where the rule will be applied."),
                               required=True,
                               widget=forms.Select(choices=users_choices))

    access = forms.ChoiceField(
        label=_('Level of access'),
        choices=[('list', _('List')),
                 ('read', _('Read-only')),
                 ('read-write', _('Read and Write'))],
        initial='list'
    )

    object_type_choices = []
    object_type = forms.ChoiceField(choices=object_type_choices,
                                    label=_("Read Condition: Object Type"),
                                    help_text=_("The type of object the rule will be applied to."),
                                    required=False)

    object_tag = forms.CharField(max_length=255,
                                 label=_("Read Condition: Object Tag"),
                                 required=False,
                                 help_text=_("The metadata tag of object the rule will be applied to."))

    def __init__(self, request, *args, **kwargs):
        # Obtain list of projects
        self.project_choices = [('', 'Select one'), common.get_project_list_choices(request)]

        self.object_type_choices = common.get_object_type_choices(request)

        # Initialization
        super(CreateAccessControlPolicy, self).__init__(request, *args, **kwargs)

        # Overwrite project_id input form
        self.fields['project_id'] = forms.ChoiceField(choices=self.project_choices,
                                                      label=_("Project"),
                                                      help_text=_("The project where the rule will be apply."),
                                                      required=True)

        self.fields['object_type'] = forms.ChoiceField(choices=self.object_type_choices,
                                                       label=_("Read Condition: Object Type"),
                                                       help_text=_("The type of object the rule will be applied to."),
                                                       required=False)

    @staticmethod
    def handle(request, data):
        try:
            response = api.create_access_control_policy(request, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully created access control policy'))
                return data
            else:
                raise ValueError(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:policies:index")
            error_message = "Unable to create access control policy.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdateAccessControlPolicy(forms.SelfHandlingForm):

    access = forms.ChoiceField()

    object_type_choices = []
    object_type = forms.ChoiceField(choices=object_type_choices,
                                    label=_("Read Condition: Object Type"),
                                    help_text=_("The type of object the rule will be applied to."),
                                    required=False)

    object_tag = forms.CharField(max_length=255,
                                 label=_("Read Condition: Object Tag"),
                                 required=False,
                                 help_text=_("The metadata tag of object the rule will be applied to."))

    def __init__(self, request, *args, **kwargs):        
        super(UpdateAccessControlPolicy, self).__init__(request, *args, **kwargs)

        initial_value = ''
        if self.initial['read'] and self.initial['write']:
            initial_value = 'read-write'
        elif self.initial['read']:
            initial_value = 'read'
        elif self.initial['list']:
            initial_value = 'list'

        self.fields['access'] = forms.ChoiceField(
            label=_('Level of access'),
            choices=[('list', _('List')),
                 ('read', _('Read-only')),
                 ('read-write', _('Read and Write'))],
            initial=initial_value
        )        

        self.object_type_choices = common.get_object_type_choices(request)
        self.fields['object_type'] = forms.ChoiceField(choices=self.object_type_choices,
                                                       label=_("Read Condition: Object Type"),
                                                       help_text=_("The type of object the rule will be applied to."),
                                                       required=False)

    def handle(self, request, data):
        try:
            acl_id = self.initial["policy_id"]
            response = api.update_access_control_policy(request, data, acl_id)
            if 200 > response.status_code >= 300:
                raise sdsexception.SdsException(response)
            else:
                messages.success(request, _('Successfully updated policy: %s') % self.initial['policy_id'])
                return data
        except Exception as ex:
            redirect = reverse("horizon:crystal:policies:index")
            error_message = "Unable to update ACL.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
