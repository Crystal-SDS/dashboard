import sys
from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError  # noqa
from django.core.urlresolvers import reverse
from horizon import exceptions
from horizon import forms
from horizon import messages

import json

from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from crystal_dashboard.api import crystal as api


class CreateZone(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the new zone."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))
    description = forms.CharField(max_length=255,
                                  label=_("Description"),
                                  help_text=_("The description of the new Zone"),
                                  widget=forms.TextInput(
                                      attrs={"ng-model": "description", "not-blank": ""}
                                  ))

    def __init__(self, request, *args, **kwargs):
        super(CreateZone, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            response = api.new_zone(request, data)
            if 200 <= response.status_code < 300:
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:zones:index")
            error_message = "Unable to create the new zone.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)


class UpdateZone(forms.SelfHandlingForm):
    
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the new zone."))
                           
    description = forms.CharField(max_length=255,
                                  label=_("Description"),
                                  help_text=_("The description of the new Zone"))
    
    zone_id = forms.CharField(max_length=255,
                             label=_("Zone ID"),
                             widget=forms.HiddenInput())

    def __init__(self, request, *args, **kwargs):
        super(UpdateZone, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            response = api.update_zone(request, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully updated node: %s') % data['zone_id'])
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:zones:index")
            error_message = "Unable to update zone.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)