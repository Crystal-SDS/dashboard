from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import forms
from crystal_dashboard.dashboards.sdscontroller.bandwidth_differentiation.controllers import forms as controllers_forms


class CreateGETView(forms.ModalFormView):
    form_class = controllers_forms.CreateGETController
    form_id = "create_get_form"

    modal_header = _("Create Controller")
    submit_label = _("Create Controller")
    submit_url = reverse_lazy("horizon:sdscontroller:bandwidth_differentiation:controllers:create_get_controller")
    template_name = "sdscontroller/bandwidth_differentiation/controllers/create.html"
    context_object_name = "controller"
    success_url = reverse_lazy("horizon:sdscontroller:bandwidth_differentiation:index")
    page_title = _("Create Controller")


class CreatePUTView(forms.ModalFormView):
    form_class = controllers_forms.CreatePUTController
    form_id = "create_put_form"

    modal_header = _("Create Controller")
    submit_label = _("Create Controller")
    submit_url = reverse_lazy("horizon:sdscontroller:bandwidth_differentiation:controllers:create_put_controller")
    template_name = "sdscontroller/bandwidth_differentiation/controllers/create.html"
    context_object_name = "controller"
    success_url = reverse_lazy("horizon:sdscontroller:bandwidth_differentiation:index")
    page_title = _("Create Controller")


class CreateReplicationView(forms.ModalFormView):
    form_class = controllers_forms.CreateReplicationController
    form_id = "create_replication_form"

    modal_header = _("Create Controller")
    submit_label = _("Create Controller")
    submit_url = reverse_lazy("horizon:sdscontroller:bandwidth_differentiation:controllers:create_replication_controller")
    template_name = "sdscontroller/bandwidth_differentiation/controllers/create.html"
    context_object_name = "controller"
    success_url = reverse_lazy("horizon:sdscontroller:bandwidth_differentiation:index")
    page_title = _("Create Controller")
