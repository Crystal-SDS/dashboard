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

    analyzer_choices = []
    analyzer_id = forms.ChoiceField(choices=analyzer_choices,
                                    label=_('Analyzer'),
                                    help_text=_("The analyzer assigned to the submitted job."),
                                    required=True,
                                    widget=forms.ThemableSelectWidget(attrs={
                                        'class': 'switchable',
                                        'data-slug': 'analyzer_id'})
                                    )
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

    executor_cores = forms.CharField(label=_("Executor cores"),
                                     required=False,
                                     )

    executor_memory = forms.CharField(label=_("Executor memory"),
                                      required=False,
                                      )

    parallelism = forms.CharField(label=_("Parallelism"),
                                  required=False,
                                  )

    arguments = forms.CharField(label=_("Arguments"),
                                required=False,
                                )

    pushdown = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kwargs):
        # Obtain list of projects

        self.tenant_choices = [('', 'Select one'), common.get_project_list_choices(request)]
        # self.container_choices = common.get_container_list_choices(request, request.user.project_id)  # Default: containers from current project
        # self.analyzer_choices = common.get_anj_analyzer_list_choices(request)
        analyzer_list = common.get_anj_analyzer_list(request)
        self.analyzer_choices = [('', 'Select one')]
        self.analyzer_choices.extend(analyzer_list)

        super(SubmitJob, self).__init__(request, *args, **kwargs)

        # Overwrite filter_id input form
        self.fields['analyzer_id'] = forms.ChoiceField(choices=self.analyzer_choices,
                                                       label=_('Analyzer'),
                                                       help_text=_("The analyzer assigned to the submitted job."),
                                                       required=True,
                                                       widget=forms.ThemableSelectWidget(attrs={
                                                           'class': 'switchable',
                                                           'data-slug': 'analyzer_id'})
                                                       )

        # Overwrite tenant_id input form
        self.fields['tenant_id'] = forms.ChoiceField(choices=self.tenant_choices,
                                                     initial=request.user.project_id,  # Default project is the current one
                                                     label=_("Project"),
                                                     help_text=_("The project assigned to the submitted job."),
                                                     required=True)

        analyzers_ids = {'Spark': 'dummy', 'Flink': 'dummy'}
        for analyzer in analyzer_list:
            if 'Spark' in analyzer[1]:
                analyzers_ids['Spark'] = analyzer[0]  # analyzer id
            elif 'Flink' in analyzer[1]:
                analyzers_ids['Flink'] = analyzer[0]  # analyzer id

        self.fields['executor_cores'] = forms.CharField(label=_("Executor cores"),
                                                        help_text=_("The number of cores to use on each executor."),
                                                        required=False,
                                                        widget=forms.TextInput(
                                                            attrs={'class': 'switched',
                                                                   'data-switch-on': 'analyzer_id',
                                                                   'data-analyzer_id-' + analyzers_ids['Spark']: _("Executor cores")})
                                                        )

        self.fields['executor_memory'] = forms.CharField(label=_("Executor memory"),
                                                         help_text=_("Amount of memory to use per executor process (e.g. 2g, 8g)"),
                                                         required=False,
                                                         widget=forms.TextInput(
                                                             attrs={'class': 'switched',
                                                                    'data-switch-on': 'analyzer_id',
                                                                    'data-analyzer_id-' + analyzers_ids['Spark']: _("Executor memory")})
                                                         )

        self.fields['parallelism'] = forms.CharField(label=_("Parallelism"),
                                                     help_text=_("The parallelism with which to run the program."),
                                                     required=False,
                                                     widget=forms.TextInput(
                                                         attrs={'class': 'switched',
                                                                'data-switch-on': 'analyzer_id',
                                                                'data-analyzer_id-' + analyzers_ids['Flink']: _("Parallelism")})
                                                     )

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
