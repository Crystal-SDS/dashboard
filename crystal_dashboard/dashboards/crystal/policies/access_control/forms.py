from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from crystal_dashboard.api import policies as api
from crystal_dashboard.dashboards.crystal import common
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class CreateAccessControlPolicy(forms.SelfHandlingForm):
    project_choices = []
    project_id = forms.ChoiceField(choices=project_choices,
                                   label=_("Project"),
                                   help_text=_("The project where the rule will be applied."),
                                   required=True)

    policy_choices = []
    policy_id = forms.ChoiceField(choices=policy_choices,
                                  label=_("Storage Policy (Ring)"),
                                  help_text=_("The storage policy that you want to assign to the specific project."),
                                  required=True)

    get_bandwidth = forms.CharField(max_length=255,
                                    label=_("GET Bandwidth"),
                                    help_text=_("The GET bandwidth that you want to assign to the specific project."),
                                    widget=forms.TextInput(
                                        attrs={"ng-model": "get_bandwidth", "not-blank": ""}
                                    ))
    put_bandwidth = forms.CharField(max_length=255,
                                    label=_("PUT Bandwidth"),
                                    help_text=_("The PUT bandwidth that you want to assign to the specific project."),
                                    widget=forms.TextInput(
                                        attrs={"ng-model": "put_bandwidth", "not-blank": ""}
                                    ))

    def __init__(self, request, *args, **kwargs):
        # Obtain list of projects
        self.project_choices = [('', 'Select one'), common.get_project_list_choices(request)]
        # Obtain list of storage policies
        self.storage_policy_choices = common.get_storage_policy_list_choices(request, common.ListOptions.by_id())

        # Initialization
        super(CreateAccessControlPolicy, self).__init__(request, *args, **kwargs)

        # Overwrite target_id input form
        self.fields['project_id'] = forms.ChoiceField(choices=self.project_choices,
                                                      label=_("Project"),
                                                      help_text=_("The target project for this SLO."),
                                                      required=True)

        self.fields['policy_id'] = forms.ChoiceField(choices=self.storage_policy_choices,
                                                     label=_("Storage Policy (Ring)"),
                                                     help_text=_("The target storage policy for this SLO."),
                                                     required=True)

    @staticmethod
    def handle(request, data):

        try:
            target = data['project_id'] + '#' + data['policy_id']
            data_get = {'dsl_filter': 'bandwidth', 'slo_name': 'get_bw', 'target': target, 'value': data['get_bandwidth']}
            data_put = {'dsl_filter': 'bandwidth', 'slo_name': 'put_bw', 'target': target, 'value': data['put_bandwidth']}
            response_get = api.fil_add_slo(request, data_get)
            response_put = api.fil_add_slo(request, data_put)

            if (200 <= response_get.status_code < 300) and (200 <= response_put.status_code < 300):
                messages.success(request, _("SLO successfully created."))
                return data
            else:
                raise sdsexception.SdsException("Get SLO: "+response_get.text + "Put SLO: "+response_get.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:policies:index")
            error_message = "Unable to create SLO.\t %s" % ex.message
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
