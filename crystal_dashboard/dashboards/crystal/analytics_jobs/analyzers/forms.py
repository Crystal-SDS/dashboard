from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from crystal_dashboard.api import analytics as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class CreateAnalyzer(forms.SelfHandlingForm):
    analyzer_file = forms.FileField(label=_("File"), required=True, allow_empty_file=False)
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the analyzer to be created."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))
    framework = forms.ChoiceField(
        label=_('Framework'),
        choices=[('Spark', _('Spark')),
                 ('Flink', _('Flink')),
                 ('Others', _('Others'))],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )
    job_language = forms.CharField(max_length=255,
                           label=_("Job language"),
                           help_text=_("The job programming language this analyzer was created for."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "job_language", "not-blank": ""}
                           ))

    def __init__(self, request, *args, **kwargs):
        super(CreateAnalyzer, self).__init__(request, *args, **kwargs)


    @staticmethod
    def handle(request, data):
        analyzer_file = data['analyzer_file']
        del data['analyzer_file']

        try:
            response = api.anj_add_analyzer(request, data, analyzer_file)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully created filter: %s') % data['name'])
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:analytics_jobs:index")
            error_message = "Unable to create analyzer.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
