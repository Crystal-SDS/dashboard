"""
Forms for managing object types.
"""
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from crystal_dashboard.api import policies as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class CreateObjectType(forms.SelfHandlingForm):
    filter_list = []

    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the Object Type to be created."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))
    extensions = forms.CharField(max_length=255,
                           label=_("Extensions"),
                           required=True,
                           help_text=_("A comma separated list of file extensions to include in this object type. Ex: doc, docx, xls, xlsx"),
                           widget=forms.TextInput(
                               attrs={"ng-model": "extensions"}
                           ))

    def __init__(self, request, *args, **kwargs):
        super(CreateObjectType, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        name = data["name"]
        extensions = [x.strip() for x in data["extensions"].split(',')]

        try:
            response = api.dsl_create_object_type(request, name, extensions)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully created object type: %s') % data['name'])
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:policies:index")
            error_message = "Unable to create object type.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdateObjectType(forms.SelfHandlingForm):
    filter_list = []

    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    extensions = forms.CharField(max_length=255,
                             label=_("Extensions"),
                             required=True,
                             help_text=_(
                                 "A comma separated list of file extensions to include in this object type. Ex: doc, docx, xls, xlsx"),
                             )

    def __init__(self, request, *args, **kwargs):
        super(UpdateObjectType, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        name = data["name"]

        try:
            extensions = [x.strip() for x in data["extensions"].split(',')]
            response = api.dsl_update_object_type(request, name, extensions)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully updated object type: %s') % data['name'])
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:policies:index")
            error_message = "Unable to update object type.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
