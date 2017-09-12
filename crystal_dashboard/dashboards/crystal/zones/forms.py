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
    zone_id = forms.CharField(max_length=5,
                                label=_("Zone ID"),
                                help_text=_("The unique ID to identify the zone."),
                                widget=forms.TextInput(
                                    attrs={"ng-model": "zone_id", "not-blank": ""}
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

        #TODO: After rebuild the form this code should disappear
        try:
            storage_nodes_response = api.list_storage_nodes(request)
            if storage_nodes_response.text:
                storage_nodes = json.loads(storage_nodes_response.text)
                storage_nodes_form = data['storage_node'].split(',')
                data["storage_node"] = {}
                for i in range(0, len(storage_nodes_form), 2):
                    for storage_node in storage_nodes:
                        if storage_node["id"] == storage_nodes_form[i]:
                            location = storage_node['location']
                            data["storage_node"][location] = storage_nodes_form[i+1]
            else:
                raise Exception
        except Exception, e:
            redirect = reverse("horizon:crystal:rings_and_accounts:index")
            error_message = "Storage nodes not found"
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)
        try:
            response = api.new_storage_policy(request, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully EC Storage Policy created.'))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:rings_and_accounts:index")
            error_message = "Unable to EC Storage Policy.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)