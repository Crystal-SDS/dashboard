from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from crystal_dashboard.api import policies as api
from crystal_dashboard.dashboards.crystal import common
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from openstack_dashboard import api as api_keystone
from openstack_dashboard.utils import identity


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

    users_choices = []
    user_id = forms.ChoiceField(choices=users_choices,
                                label=_("Users"),
                                required=True)

    write = forms.BooleanField(required=False, label="Write")
    read = forms.BooleanField(required=False, label="Read")

    object_type_choices = []
    object_type = forms.ChoiceField(choices=object_type_choices,
                                    label=_("Object Type"),
                                    help_text=_("The type of object the rule will be applied to."),
                                    required=False)

    object_tag = forms.CharField(max_length=255,
                                 label=_("Object Tag"),
                                 required=False,
                                 help_text=_("The metadata tag of object the rule will be applied to."))

    def __init__(self, request, *args, **kwargs):
        # Obtain list of projects
        self.project_choices = [('', 'Select one'), ('global', 'Global (All Projects)'), common.get_project_list_choices(request), common.get_group_project_choices(request)]

        self.container_choices = common.get_container_list_choices(request)  # Default: containers from current project

        self.object_type_choices = common.get_object_type_choices(request)

        # Initialization
        super(CreateAccessControlPolicy, self).__init__(request, *args, **kwargs)

        # Overwrite project_id input form
        self.fields['project_id'] = forms.ChoiceField(choices=self.project_choices,
                                                      initial=request.user.project_id,  # Default project is the current one
                                                      label=_("Project"),
                                                      help_text=_("The project where the rule will be apply."),
                                                      required=True)

        # Overwrite contained_id input form
        self.fields['container_id'] = forms.ChoiceField(choices=self.container_choices,
                                                        label=_("Container"),
                                                        help_text=_("The container where the rule will be apply."),
                                                        required=False)

        project = self.fields['project_id'].initial
        users = [(user.id, user.name) for user in api_keystone.keystone.user_list(request, project=project)]
        self.users_choices = [('', 'Select one'), ('Users', users)]

        self.fields['user_id'] = forms.ChoiceField(choices=self.users_choices,
                                                   label=_("Users"),
                                                   required=True)

        self.fields['object_type'] = forms.ChoiceField(choices=self.object_type_choices,
                                                       label=_("Object Type"),
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
            error_message = "Unable to create access control policy/rule.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdateAccessControlPolicy(forms.SelfHandlingForm):
    get_bandwidth = forms.CharField(max_length=255,
                                    label=_("GET Bandwidth"),
                                    required=False,
                                    help_text=_("The GET bandwidth that you want to assign to the specific project."))
    put_bandwidth = forms.CharField(max_length=255,
                                    label=_("PUT Bandwidth"),
                                    required=False,
                                    help_text=_("The PUT bandwidth that you want to assign to the specific project."))

    def __init__(self, request, *args, **kwargs):
        super(UpdateAccessControlPolicy, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            sla_id = self.initial["id"]
            ok = True
            error_msg = ""
            if self.initial["get_bandwidth"] != data['get_bandwidth']:
                response = api.fil_update_slo(request, 'bandwidth', 'get_bw', sla_id, {'value': data['get_bandwidth']})
                if 200 > response.status_code >= 300:
                    ok = False
                    error_msg = response.text
            if self.initial["put_bandwidth"] != data['put_bandwidth']:
                response = api.fil_update_slo(request, 'bandwidth', 'put_bw', sla_id, {'value': data['put_bandwidth']})
                if 200 > response.status_code >= 300:
                    ok = False
                    error_msg = response.text
            if ok:
                messages.success(request, _("Successfully update SLO."))
                return data
            else:
                raise sdsexception.SdsException(error_msg)
        except Exception as ex:
            redirect = reverse("horizon:crystal:policies:index")
            error_message = "Unable to update SLO.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
