from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError  # noqa
from django.core.urlresolvers import reverse
from horizon import exceptions
from horizon import forms
from horizon import messages
import json

from crystal_dashboard.dashboards.crystal import exceptions as sdsexception
from crystal_dashboard.api import swift as api


class CreateStoragePolicy(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the new policy."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))

    replicas = forms.CharField(max_length=255,
                               label=_("Num. Replicas"),
                               help_text=_("Number of replicas"),
                               initial=3)
 
    partition_power = forms.CharField(max_length=255,
                                      label=_("Partiton Power"),
                                      help_text=_("If the value is x the num of partitions will be 2^x"),
                                      initial=10)
 
    time = forms.CharField(max_length=255,
                           label=_("Time"),
                           help_text=_("Time between moving a partition more than once. In hours"),
                           initial=1)
    
    
    policy_type = forms.CharField(widget=forms.HiddenInput(), initial='replication')
 
    deprecated = forms.CharField(widget=forms.HiddenInput(), initial='False')
  
    deployed = forms.CharField(widget=forms.HiddenInput(), initial='False')
    
    default = forms.CharField(widget=forms.HiddenInput(), initial='False')
      
    devices = forms.CharField(widget=forms.HiddenInput(), initial='[]')

    def __init__(self, request, *args, **kwargs):
        super(CreateStoragePolicy, self).__init__(request, *args, **kwargs)


    def handle(self, request, data):
        try:
            response = api.swift_new_storage_policy(request, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _("Storage policy successfully created."))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:rings:index")
            error_message = "Unable to create storage policy.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
        


class UpdateStoragePolicy(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the new policy."))

    default = forms.BooleanField(required=False, label="Default")
    deprecated = forms.BooleanField(required=False, label="Deprecated")



    def __init__(self, request, *args, **kwargs):
        super(UpdateStoragePolicy, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            response = api.swift_edit_storage_policy(request, self.initial['storage_policy_id'], data)
            if 200 <= response.status_code < 300:
                messages.success(request, _("Storage policy successfully updated."))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:rings:index")
            error_message = "Unable to update storage policy.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class CreateECStoragePolicy(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the new policy."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))

    partition_power = forms.CharField(max_length=255,
                                      label=_("Partiton Power"),
                                      help_text=_("If the value is x the num of partitions will be 2^x"),
                                      initial=10)

    time = forms.CharField(max_length=255,
                           label=_("Time"),
                           help_text=_("Time between moving a partition more than once. In hours"),
                           initial=1)

    ec_type = forms.CharField(max_length=255,
                              label=_("EC Type"),
                              required=True,
                              help_text=_("Is chosen from the list of EC backends supported by PyECLib"),
                              initial='liberasurecode_rs_vand')

    ec_num_data_fragments = forms.CharField(max_length=255,
                                            label=_("Num. Data Fragments"),
                                            required=True,
                                            help_text=_("The total number of fragments that will be comprised of data."),
                                            initial=10)

    ec_num_parity_fragments = forms.CharField(max_length=255,
                                              label=_("Num. Parity Fragments"),
                                              required=True,
                                              help_text=_("The total number of fragments that will be comprised of parity."),
                                              initial=4)

    ec_object_segment_size = forms.CharField(max_length=255,
                                             label=_("Object Segment Size"),
                                             required=True,
                                             help_text=_("The amount of data that will be buffered up before feeding a segment into the encoder/decoder."),
                                             initial=1048576)

    ec_duplication_factor = forms.CharField(max_length=255,
                                            label=_("Duplication Factor"),
                                            required=True,
                                            help_text=_("EC Duplication enables Swift to make duplicated copies of fragments of erasure coded objects."),
                                            initial=1)
    
    policy_type = forms.CharField(widget=forms.HiddenInput(), initial='EC')

    deprecated = forms.CharField(widget=forms.HiddenInput(), initial='False')
  
    deployed = forms.CharField(widget=forms.HiddenInput(), initial='False')
    
    devices = forms.CharField(widget=forms.HiddenInput(), initial='[]')
    
    default = forms.CharField(widget=forms.HiddenInput(), initial='False')


    def __init__(self, request, *args, **kwargs):
        super(CreateECStoragePolicy, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            response = api.swift_new_storage_policy(request, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _("Storage policy successfully created."))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:rings:index")
            error_message = "Unable to create storage policy.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


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
