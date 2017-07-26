from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from crystal_dashboard.api import sds_controller as api
from crystal_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class CreateSortedMethod(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Sorted Nodes Method:"),
                           help_text=_("The sorted_method name."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "sorted_nodes_method", "not-blank": ""}
                           ))

    criterion = forms.CharField(max_length=255,
                                label=_("Sorted Nodes Criterion:"),
                                help_text=_("ascending or descending ."),
                                widget=forms.TextInput(
                                    attrs={"ng-model": "sorted_nodes_criterion", "not-blank": ""}
                                ))

    def __init__(self, request, *args, **kwargs):
        super(CreateSortedMethod, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            response = api.bw_add_sort_method(request, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully sorted method creation.'))
                return data
            else:
                raise sdsexception.SdsException(response.text)

        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to create sorted method.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdateSortedMethod(forms.SelfHandlingForm):
    criterion = forms.CharField(max_length=255,
                                label=_("Criterion"),
                                required=False,
                                help_text=_("The new criterion that you want to assign."))

    def __init__(self, request, *args, **kwargs):
        super(UpdateSortedMethod, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            proxy_sorting_id = self.initial['id']
            response = api.bw_update_sort_method(request, proxy_sorting_id, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully sorted method update.'))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to update sorted method.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
