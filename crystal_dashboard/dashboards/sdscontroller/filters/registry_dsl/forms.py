from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from crystal_dashboard.api import crystal as api
from crystal_dashboard.dashboards.sdscontroller import common
from crystal_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class CreateFilter(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the filter to be created."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))

    filter_identifier = forms.ChoiceField(choices=[],
                                          label=_("Filter"),
                                          help_text=_("Filter to be used."),
                                          required=False,
                                          widget=forms.Select(
                                              attrs={"ng-model": "filter_identifiers", "not-blank": ""}
                                          ))

    activation_url = forms.CharField(max_length=255,
                                     label=_("API Activation Url"),
                                     help_text=_("API Activation Url"),
                                     initial=settings.IOSTACK_CONTROLLER_FILTERS_ENDPOINT
                                     )

    valid_parameters = forms.CharField(max_length=255,
                                       label=_("valid_parameters"),
                                       required=False,
                                       help_text=_("A comma separated list of tuples of data, as Python dictionary. Ex: param2: integer, param1: bool"),
                                       widget=forms.TextInput(
                                           attrs={"ng-model": "valid_parameters"}
                                       ))

    def __init__(self, request, *args, **kwargs):
        self.filter_list = common.get_filter_list_choices(request)
        super(CreateFilter, self).__init__(request, *args, **kwargs)
        self.fields['filter_identifier'] = forms.ChoiceField(choices=self.filter_list,
                                                             label=_("Filter"),
                                                             help_text=_("Filter to be used."),
                                                             required=False,
                                                             widget=forms.Select(
                                                                 attrs={"ng-model": "filter_identifiers", "not-blank": ""}
                                                             ))

    @staticmethod
    def handle(request, data):
        data['identifier'] = data.pop('filter_identifier')

        try:
            response = api.dsl_add_filter(request, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully created filter: %s') % data['name'])
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:filters:index")
            error_message = "Unable to create filter.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdateFilter(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           widget=forms.TextInput(
                               attrs={'readonly': 'readonly'})
                           )

    activation_url = forms.CharField(max_length=255,
                                     label=_("API Activation Url"),
                                     help_text=_("API Activation Url")
                                     )

    valid_parameters = forms.CharField(max_length=255,
                                       label=_("valid_parameters"),
                                       required=False,
                                       help_text=_("A comma separated list of tuples of data, as Python dictionary. Ex: param2: integer, param1: bool")
                                       )

    def __init__(self, request, *args, **kwargs):
        super(UpdateFilter, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):
        try:
            response = api.dsl_update_filter(request, data["name"], data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully updated filter: %s') % data['name'])
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:filters:index")
            error_message = "Unable to create filter.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
