import json

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from crystal_dashboard.api import sds_controller as api
from crystal_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class UploadDependency(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the dependency to be created. It is a unique field."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))

    version = forms.CharField(max_length=255,
                              label=_("Version"),
                              help_text=_("While the engine currently does not parse this header, it must appear."),
                              widget=forms.TextInput(
                                  attrs={"ng-model": "version", "not-blank": ""}
                              ))

    permissions = forms.CharField(max_length=255,
                                  label=_("Permissions"),
                                  required=False,
                                  help_text=_("An optional metadata field, where the user can state the permissions given to the dependency when it is copied to the Linux container. This is helpful for binary dependencies invoked by the filter. For a binary dependency once can specify: '0755'"),
                                  widget=forms.TextInput(
                                      attrs={"ng-model": "permissions"}
                                  ))

    dependency_file = forms.FileField(label=_("File"),
                                      required=True,
                                      allow_empty_file=False)

    def __init__(self, request, *args, **kwargs):
        super(UploadDependency, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):
        dependency_file = data['dependency_file']
        del data['dependency_file']

        try:
            response = api.fil_create_dependency(request, data)
            if 200 <= response.status_code < 300:
                dependency_id = json.loads(response.text)["id"]
                response = api.fil_upload_dependency_data(request, dependency_id, dependency_file)

                if 200 <= response.status_code < 300:
                    messages.success(request, _('Successfully dependency creation and upload.'))
                    return data
                else:
                    raise sdsexception.SdsException(response.text)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to create dependency.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdateDependency(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the dependency to be created. It is a unique field."),
                           widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    version = forms.CharField(max_length=255,
                              label=_("Version"),
                              help_text=_("While the engine currently does not parse this header, it must appear."))

    permissions = forms.CharField(max_length=255,
                                  label=_("Permissions"),
                                  required=False,
                                  help_text=_("An optional metadata field, where the user can state the permissions given to the dependency when it is copied to the Linux container. This is helpful for binary dependencies invoked by the filter. For a binary dependency once can specify: '0755'"))

    def __init__(self, request, *args, **kwargs):
        super(UpdateDependency, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            dependency_id = self.initial['id']
            # print "\n#################\n", request, "\n#################\n", data, "\n#################\n"
            response = api.fil_update_dependency_metadata(request, dependency_id, data['version'], data['permissions'])
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully dependency creation and upload.'))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to create dependency.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
