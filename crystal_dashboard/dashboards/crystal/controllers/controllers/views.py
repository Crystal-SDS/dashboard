from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import forms
from crystal_dashboard.dashboards.crystal.controllers.controllers import forms as controllers_forms


class CreateControllerView(forms.ModalFormView):
    form_class = controllers_forms.CreateController
    form_id = "create_controller_form"

    modal_header = _("Create Controller")
    submit_label = _("Create Controller")
    submit_url = reverse_lazy("horizon:crystal:controllers:controllers:create_controller")
    template_name = "crystal/controllers/controllers/create.html"
    context_object_name = "controller"
    success_url = reverse_lazy("horizon:crystal:controllers:index")
    page_title = _("Create Controller")
