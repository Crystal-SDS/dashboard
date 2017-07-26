# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Views for managing object types.
"""
import json

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from horizon import forms
from horizon.utils import memoized
from horizon import exceptions

from openstack_dashboard.dashboards.sdscontroller.administration.object_types \
    import forms as ot_forms
from openstack_dashboard.api import sds_controller as api


class CreateObjectTypeView(forms.ModalFormView):
    form_class = ot_forms.CreateObjectType
    modal_header = _("Create Object Type")
    modal_id = "create_object_type_modal"
    template_name = 'sdscontroller/administration/object_types/create.html'
    success_url = reverse_lazy('horizon:sdscontroller:administration:index')
    page_title = _("Create an Object Type")
    submit_label = _("Create")
    submit_url = reverse_lazy(
        "horizon:sdscontroller:administration:object_types:create")

class UpdateObjectTypeView(forms.ModalFormView):
    form_class = ot_forms.UpdateObjectType
    form_id = "update_object_type_form"
    modal_header = _("Update Object Type")
    submit_label = _("Update Object Type")
    submit_url = "horizon:sdscontroller:administration:object_types:update"
    template_name = "sdscontroller/administration/object_types/update.html"
    context_object_name = 'object_type'
    success_url = reverse_lazy('horizon:sdscontroller:administration:index')
    page_title = _("Update Object Type")

    def get_context_data(self, **kwargs):
        context = super(UpdateObjectTypeView, self).get_context_data(**kwargs)
        context['object_type_id'] = self.kwargs['object_type_id']
        args = (self.kwargs['object_type_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        name = self.kwargs['object_type_id']
        try:
            object_type = api.dsl_get_object_type(self.request, name)
            return object_type
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve object type details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        object_type = self._get_object()
        name = self.kwargs['object_type_id']
        initial = json.loads(object_type.text)
        initial['name'] = name
        initial['extensions'] = ', '.join(initial['types_list'])
        return initial
