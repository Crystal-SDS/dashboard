from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError  # noqa
from django.core.urlresolvers import reverse
from horizon import exceptions
from horizon import forms
from horizon import messages
import json

from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from crystal_dashboard.api import swift as api


class CreateECStoragePolicy(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the new policy."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))
    
    ec_type = forms.CharField(max_length=255,
                              label=_("EC Type"),
                              required=False,
                              help_text=_("Is chosen from the list of EC backends supported by PyECLib"),
                              widget=forms.TextInput(
                                  attrs={"ng-model": "ec_type", "not-blank": ""}
                              ))

    ec_num_data_fragments = forms.CharField(max_length=255,
                                            label=_("Num. Data Fragments"),
                                            required=False,
                                            help_text=_("Num. Data Fragments"),
                                            widget=forms.TextInput(
                                                attrs={"ng-model": "ec_num_data_fragments", "not-blank": ""}
                                            ))

    ec_num_parity_fragments = forms.CharField(max_length=255,
                                              label=_("Num. Parity Fragments"),
                                              required=False,
                                              help_text=_("Num parity fragments"),
                                              widget=forms.TextInput(
                                                  attrs={"ng-model": "ec_num_parity_fragments", "not-blank": ""}
                                              ))

    ec_object_segment_size = forms.CharField(max_length=255,
                                             label=_("Object Segment Size"),
                                             required=False,
                                             help_text=_("Object Segment Size"),
                                             widget=forms.TextInput(
                                                 attrs={"ng-model": "ec_object_segment_size", "not-blank": ""}
                                             ))

    partitions = forms.CharField(max_length=255,
                                 label=_("Num. Partitions"),
                                 required=False,
                                 help_text=_("If the value is x the num of partitions will be 2^x"),
                                 widget=forms.TextInput(
                                     attrs={"ng-model": "partitions", "not-blank": ""}
                                 ))

    time = forms.CharField(max_length=255,
                           label=_("Time"),
                           required=False,
                           help_text=_("Time between moving a partition more than once. In hours"),
                           widget=forms.TextInput(
                               attrs={"ng-model": "time", "not-blank": ""}
                           ))

    def __init__(self, request, *args, **kwargs):
        super(CreateECStoragePolicy, self).__init__(request, *args, **kwargs)

    # def _set_filter_path(self, data):
    #     if data['path']:
    #         filter_path = "/".join([data['path'].rstrip("/"), data['name']])
    #     else:
    #         filter_path = data['name']
    #     return filter_path

    # def clean(self):
    #     data = super(UploadFilter, self).clean()
    #
    #     image_file = data.get('filter_file', None)
    #     image_url = data.get('image_url', None)
    #
    #     if not image_url and not image_file:
    #         raise ValidationError(
    #             _("A external file must be specified."))
    #     else:
    #         return data

    def handle(self, request, data):

        # TODO: After rebuild the form this code should disappear
        try:
            storage_nodes_response = api.list_storage_nodes(request)

            if storage_nodes_response.text:
                storage_nodes = json.loads(storage_nodes_response.text)
                storage_nodes_form = data['storage_node'].split(',')
                data["storage_node"] = {}
                for i in range(0, len(storage_nodes_form), 2):
                    location = str(storage_nodes[int(storage_nodes_form[i]) - 1]['location'])
                    data["storage_node"][location] = storage_nodes_form[i + 1]
            else:
                raise Exception
        except Exception, e:
            redirect = reverse("horizon:crystal:rings_and_accounts:index")
            error_message = "Storage nodes not found"
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)

        try:
            data['replicas'] = int(data["ec_num_data_fragments"]) + int(data["ec_num_parity_fragments"])
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


class LoadSwiftPolicies(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name assigned to new storage node."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))
    type = forms.CharField(max_length=255,
                           label=_("Type"),
                           help_text=_("SSD or HDD"),
                           widget=forms.TextInput(
                               attrs={"ng-model": "type", "not-blank": ""}
                           ))

    def __init__(self, request, *args, **kwargs):
        super(LoadSwiftPolicies, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        api.load_swift_policies(request, data)
        return data
