from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError  # noqa
from django.core.urlresolvers import reverse
from horizon import exceptions
from horizon import forms
from horizon import messages

from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from crystal_dashboard.api import swift as api


class CreateRegion(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the new region."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))
    description = forms.CharField(widget=forms.widgets.Textarea(
                                  attrs={'rows': 4}),
                                  label=_("Description"),
                                  required=False)

    def __init__(self, request, *args, **kwargs):
        super(CreateRegion, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            response = api.new_region(request, data)
            if 200 <= response.status_code < 300:
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:regions:index")
            error_message = "Unable to create the new region.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)


class UpdateRegion(forms.SelfHandlingForm):

    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the new region."))

    description = forms.CharField(widget=forms.widgets.Textarea(
                                  attrs={'rows': 4}),
                                  label=_("Description"),
                                  required=False)

    region_id = forms.CharField(max_length=255,
                                label=_("Region ID"),
                                widget=forms.HiddenInput())

    def __init__(self, request, *args, **kwargs):
        super(UpdateRegion, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            response = api.update_region(request, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully updated node: %s') % data['region_id'])
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:regions:index")
            error_message = "Unable to update region.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
