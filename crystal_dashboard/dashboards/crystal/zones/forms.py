from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError  # noqa
from django.core.urlresolvers import reverse
from horizon import exceptions
from horizon import forms
from horizon import messages

import json

from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from crystal_dashboard.api import swift as api


class CreateZone(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the new zone."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))

    region = forms.ThemableChoiceField(label=_("Region"))

    description = forms.CharField(widget=forms.widgets.Textarea(
                                  attrs={'rows': 4}),
                                  label=_("Description"),
                                  required=False)

    def __init__(self, request, *args, **kwargs):
        super(CreateZone, self).__init__(request, *args, **kwargs)
        regions = json.loads(api.swift_list_regions(request).text)
        self.fields['region'].choices = [(region['id'], region['name']) for region in regions]

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

    regions = forms.ThemableChoiceField(label=_("Region"))

    description = forms.CharField(widget=forms.widgets.Textarea(
                                  attrs={'rows': 4}),
                                  label=_("Description"),
                                  required=False)

    zone_id = forms.CharField(max_length=255,
                              label=_("Zone ID"),
                              widget=forms.HiddenInput())

    def __init__(self, request, *args, **kwargs):
        super(UpdateZone, self).__init__(request, *args, **kwargs)
        self.fields['regions'].choices = [(region['id'], region['name']) for region in json.loads(api.swift_list_regions(self.request).text)]

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
