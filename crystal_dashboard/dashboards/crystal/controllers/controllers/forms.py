from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from crystal_dashboard.api import controllers as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class CreateController(forms.SelfHandlingForm):
    controller_file = forms.FileField(label=_("File"), required=True, allow_empty_file=False)
    class_name = forms.CharField(max_length=255,
                                 label=_('Main Class'),
                                 help_text=_('The class name of the controller to be created.'),
                                 widget=forms.TextInput(
                                     attrs={'ng-model': 'name', 'not-blank': ''}
                                 ))

    description = forms.CharField(widget=forms.widgets.Textarea(
                                  attrs={'rows': 4}),
                                  label=_("Description"),
                                  required=False)

    enabled = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kwargs):
        super(CreateController, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):

        controller_file = data['controller_file']
        del data['controller_file']

        try:
            response = api.add_controller(request, data, controller_file)
            if 200 <= response.status_code < 300:
                messages.success(request, _("Controller successfully created."))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:controllers:index")
            error_message = "Unable to create controller.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdateController(forms.SelfHandlingForm):

    controller_file = forms.FileField(label=_("File"),
                                      required=False,
                                      allow_empty_file=False)

    class_name = forms.CharField(max_length=255,
                                 label=_('Class Name'),
                                 help_text=_('The class name of the controller to be created.'))

    description = forms.CharField(widget=forms.widgets.Textarea(
                                  attrs={'rows': 4}),
                                  label=_("Description"),
                                  required=False)

    enabled = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kwargs):
        super(UpdateController, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            response = api.update_controller(request, self.initial['id'], data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully updated controller: %s') % self.initial['id'])
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:controllers:index")
            error_message = "Unable to update controller.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
