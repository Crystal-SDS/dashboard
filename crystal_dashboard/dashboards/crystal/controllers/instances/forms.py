from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
import json
from horizon import exceptions
from horizon import forms
from horizon import messages
from crystal_dashboard.api import controllers as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class CreateInstance(forms.SelfHandlingForm):

    controller = forms.ThemableChoiceField(label=_("Controller"))

    parameters = forms.CharField(widget=forms.widgets.Textarea(
                                 attrs={'rows': 2}),
                                 label=_("Parameters"),
                                 required=False)

    description = forms.CharField(widget=forms.widgets.Textarea(
                                  attrs={'rows': 4}),
                                  label=_("Description"),
                                  required=False)

    status = forms.CharField(max_length=255,
                             label=_("Status"),
                             initial='Stopped',
                             widget=forms.HiddenInput(  # hidden
                                    attrs={"ng-model": "status"}))

    def __init__(self, request, *args, **kwargs):
        super(CreateInstance, self).__init__(request, *args, **kwargs)
        controllers = json.loads(api.get_all_controllers(self.request).text)
        self.fields['controller'].choices = [(controller['id'], controller['controller_name']) for controller in controllers]

    @staticmethod
    def handle(request, data):
        try:
            response = api.add_instance(request, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _("Instance successfully created."))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:controllers:index")
            error_message = "Unable to create instance.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdateInstance(forms.SelfHandlingForm):

    parameters = forms.CharField(widget=forms.widgets.Textarea(
                                 attrs={'rows': 2}),
                                 label=_("Parameters"),
                                 required=False)

    description = forms.CharField(widget=forms.widgets.Textarea(
                                  attrs={'rows': 4}),
                                  label=_("Description"),
                                  required=False)

    def __init__(self, request, *args, **kwargs):
        super(UpdateInstance, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        # try:
        response = api.update_instance(request, self.initial['id'], data)
        if 200 <= response.status_code < 300:
            messages.success(request, _('Successfully updated instance: %s') % self.initial['id'])
            return data
        else:
            raise sdsexception.SdsException(response.text)
#         except Exception as ex:
#             redirect = reverse("horizon:crystal:controllers:index")
#             error_message = "Unable to update instance.\t %s" % ex.message
#             exceptions.handle(request, _(error_message), redirect=redirect)
