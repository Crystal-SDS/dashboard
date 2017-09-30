"""
Views for managing Ring & Storage Policies.
"""
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from horizon import forms
from horizon import workflows
from crystal_dashboard.dashboards.crystal.rings.storage_policies import forms as storage_policies_forms
from crystal_dashboard.dashboards.crystal.rings.storage_policies.workflows import CreateStoragePolicyClass


# class CreateStoragePolicy(forms.ModalFormView):
#     form_class = storage_policies_forms.CreateStoragePolicy
#     form_id = "create_storage_policy_form"
#
#     modal_header = _("Create a Storage Policy")
#     submit_label = _("Create a Storage Policy")
#     submit_url = reverse_lazy('horizon:crystal:rings:storage_policies:create_storage_policy')
#     template_name = "crystal/rings/storage_policies/create_storage_policy.html"
#     context_object_name = 'storage_policy'
#     success_url = reverse_lazy('horizon:crystal:rings:index')
#     page_title = _("Create a Storage Policy")

class CreateStoragePolicy(workflows.WorkflowView):
    workflow_class = CreateStoragePolicyClass

    def get_context_data(self, **kwargs):
        context = super(CreateStoragePolicy, self).get_context_data(**kwargs)
        return context

    def _get_object(self, *args, **kwargs):
        pass

    def get_initial(self):
        initial = super(CreateStoragePolicy, self).get_initial()
        # This data will be available in the Action's methods and
        # Workflow's handle method.
        # But only if the steps will depend on them.
        return {'resource_class_id': 0}


class CreateECStoragePolicy(forms.ModalFormView):
    form_class = storage_policies_forms.CreateECStoragePolicy
    form_id = "create_ec_storage_policy_form"

    modal_header = _("Create a EC Storage Policy")
    submit_label = _("Create Storage Policy")
    submit_url = reverse_lazy('horizon:crystal:rings:storage_policies:create_ec_storage_policy')
    template_name = "crystal/rings/storage_policies/create_ec_storage_policy.html"
    context_object_name = 'storage_policy'
    success_url = reverse_lazy('horizon:crystal:rings:index')
    page_title = _("Create a Storage Policy")


class LoadSwiftPolicies(forms.ModalFormView):
    form_class = storage_policies_forms.LoadSwiftPolicies
    form_id = "load_swift_policies_form"

    modal_header = _("Load Swift Policies")
    submit_label = _("Load Swift Policies")
    submit_url = reverse_lazy('horizon:crystal:rings:storage_policies:load_swift_policies')
    template_name = "crystal/rings/storage_policies/load_swift_policies.html"
    context_object_name = 'swift_policie'
    success_url = reverse_lazy('horizon:crystal:rings:index')
    page_title = _("Load Swift Policies")
