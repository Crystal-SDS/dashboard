from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from crystal_dashboard.api import analytics as api
from crystal_dashboard.dashboards.crystal import common
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class SubmitJob(forms.SelfHandlingForm):
    job_file = forms.FileField(label=_("File"), required=True, allow_empty_file=False)
    # name = forms.CharField(max_length=255,
    #                        label=_("Name"),
    #                        help_text=_("The name of the job to submit."),
    #                        widget=forms.TextInput(
    #                            attrs={"ng-model": "name", "not-blank": ""}
    #                        ))
    analyzer_choices = []
    analyzer_id = forms.ChoiceField(choices = analyzer_choices,
                                    label=_('Analyzer'),
                                    help_text=_("The analyzer assigned to the submitted job."),
                                    required=True,)
    tenant_choices = []
    tenant_id = forms.ChoiceField(choices=tenant_choices,
                                  label=_("Project"),
                                  help_text=_("The project assigned to the submitted job."),
                                  required=True)

    # container_choices = [('', 'None')]
    # container_id = forms.CharField(label=_("Container"),
    #                                help_text=_("The container assigned to the submitted job."),
    #                                required=False,
    #                                widget=forms.Select(choices=container_choices))
    pushdown = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kwargs):
        # Obtain list of projects

        self.tenant_choices = [('', 'Select one'), common.get_project_list_choices(request)]
        self.container_choices = common.get_container_list_choices(request, request.user.project_id)  # TODO Default: containers from current project
        self.analyzer_choices = common.get_anj_analyzer_list_choices(request)

        super(SubmitJob, self).__init__(request, *args, **kwargs)

        # Overwrite tenant_id input form
        self.fields['tenant_id'] = forms.ChoiceField(choices=self.tenant_choices,
                                                     initial=request.user.project_id,  # Default project is the current one
                                                     label=_("Project"),
                                                     help_text=_("The project assigned to the submitted job."),
                                                     required=True)

        # Overwrite container_id input form
        # self.fields['container_id'] = forms.ChoiceField(choices=self.container_choices,
        #                                                 label=_("Container"),
        #                                                 help_text=_("The container assigned to the submitted job."),
        #                                                 required=False)

        # Overwrite filter_id input form
        self.fields['analyzer_id'] = forms.ChoiceField(choices=self.analyzer_choices,
                                                       label=_('Analyzer'),
                                                       help_text=_("The analyzer assigned to the submitted job."),
                                                       required=True,)


    @staticmethod
    def handle(request, data):
        job_file = data['job_file']
        del data['job_file']
        job_file_name = job_file.name

        try:
            response = api.anj_submit_job(request, data, job_file)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully submitted job: %s') % job_file_name)
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:analytics_jobs:index")
            error_message = "Unable to submit job.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
