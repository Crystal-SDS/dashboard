from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from crystal_dashboard.api import metrics as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class UploadMetricModule(forms.SelfHandlingForm):
    metric_module_file = forms.FileField(label=_("File"),
                                         required=True,
                                         allow_empty_file=False)

    class_name = forms.CharField(max_length=255,
                                 label=_("Class Name"),
                                 help_text=_("The main class of the metric module to be created."),
                                 widget=forms.TextInput(
                                     attrs={"ng-model": "name", "not-blank": ""}
                                 ))

    put = forms.BooleanField(required=False, label='Put')
    get = forms.BooleanField(required=False, label='Get')
    replicate = forms.BooleanField(required=False, label='Replicate')

    execution_server = forms.ChoiceField(
        label=_('Execution Server'),
        choices=[
            ('proxy', _('Proxy Node')),
            ('object', _('Storage Node')),
            ('proxy/object', _('Proxy & Storage Nodes'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    status = forms.CharField(max_length=255,
                             label=_("Status"),
                             initial='Stopped',
                             widget=forms.HiddenInput(  # hidden
                                attrs={"ng-model": "status"}))

    def __init__(self, request, *args, **kwargs):
        super(UploadMetricModule, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):
        metric_module_file = data['metric_module_file']
        del data['metric_module_file']

        try:
            response = api.add_metric_module_metadata(request, data, metric_module_file)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Metric module was created and uploaded successfully.'))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:metrics:index")
            error_message = "Unable to create metric module.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdateMetricModule(forms.SelfHandlingForm):
    metric_module_file = forms.FileField(label=_("File"),
                                         required=False,
                                         allow_empty_file=False)

    class_name = forms.CharField(max_length=255,
                                 label=_("Class Name"),
                                 help_text=_("The main class of the metric module to be created."))

    put = forms.BooleanField(required=False, label='Put')
    get = forms.BooleanField(required=False, label='Get')
    replicate = forms.BooleanField(required=False, label='Replicate')

    execution_server = forms.ChoiceField(
        label=_('Execution Server'),
        choices=[
            ('proxy', _('Proxy Node')),
            ('object', _('Storage Node')),
            ('proxy/object', _('Proxy & Storage Nodes'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    def __init__(self, request, *args, **kwargs):
        super(UpdateMetricModule, self).__init__(request, *args, **kwargs)

    failure_url = 'horizon:crystal:metrics:index'

    def handle(self, request, data):

        metric_module_file = data['metric_module_file']
        del data['metric_module_file']
        metric_module_id = self.initial['id']

        try:
            response = api.update_metric_module_metadata(request, metric_module_id, data)
            if 200 <= response.status_code < 300:
                try:
                    if metric_module_file is not None:
                        response = api.update_metric_module_data(request, metric_module_id, metric_module_file)
                        if response.status_code > 300:  # error
                            raise sdsexception.SdsException(response.text)
                except Exception as ex:
                    pass
                messages.success(request, _('Successfully metric module updated.'))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:metrics:index")
            error_message = "Unable to update metric module.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
