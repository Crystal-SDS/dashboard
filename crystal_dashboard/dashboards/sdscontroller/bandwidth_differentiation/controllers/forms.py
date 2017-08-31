from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from crystal_dashboard.api import crystal as api
from crystal_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class CreateGETController(forms.SelfHandlingForm):
    controller_file = forms.FileField(label=_("File"), required=True, allow_empty_file=False)
    class_name = forms.CharField(max_length=255,
                                 label=_('Class Name'),
                                 help_text=_('The class name of the controller to be created.'),
                                 widget=forms.TextInput(
                                     attrs={'ng-model': 'name', 'not-blank': ''}
                                 ))
    enabled = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kwargs):
        super(CreateGETController, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):

        controller_file = data['controller_file']
        del data['controller_file']

        try:
            data['dsl_filter'] = 'bandwidth'
            data['type'] = 'get'
            response = api.dsl_add_global_controller(request, data, controller_file)
            if 200 <= response.status_code < 300:
                messages.success(request, _("Controller successfully created."))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to create controller.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class CreatePUTController(forms.SelfHandlingForm):
    controller_file = forms.FileField(label=_("File"), required=True, allow_empty_file=False)
    class_name = forms.CharField(max_length=255,
                                 label=_('Class Name'),
                                 help_text=_('The class name of the controller to be created.'),
                                 widget=forms.TextInput(
                                     attrs={'ng-model': 'name', 'not-blank': ''}
                                 ))
    enabled = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kwargs):
        super(CreatePUTController, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):

        controller_file = data['controller_file']
        del data['controller_file']

        try:
            data['dsl_filter'] = 'bandwidth'
            data['type'] = 'put'
            response = api.dsl_add_global_controller(request, data, controller_file)
            if 200 <= response.status_code < 300:
                messages.success(request, _("Controller successfully created."))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to create controller.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class CreateReplicationController(forms.SelfHandlingForm):
    controller_file = forms.FileField(label=_("File"), required=True, allow_empty_file=False)
    class_name = forms.CharField(max_length=255,
                                 label=_('Class Name'),
                                 help_text=_('The class name of the controller to be created.'),
                                 widget=forms.TextInput(
                                     attrs={'ng-model': 'name', 'not-blank': ''}
                                 ))
    enabled = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kwargs):
        super(CreateReplicationController, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):

        controller_file = data['controller_file']
        del data['controller_file']

        try:
            data['dsl_filter'] = 'bandwidth'
            data['type'] = 'ssync'
            response = api.dsl_add_global_controller(request, data, controller_file)
            if 200 <= response.status_code < 300:
                messages.success(request, _("Controller successfully created."))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to create controller.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
