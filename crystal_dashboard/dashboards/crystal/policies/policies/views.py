import json

from django import http
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from crystal_dashboard.api import policies as api

from crystal_dashboard.dashboards.crystal import common
from crystal_dashboard.dashboards.crystal.policies.policies import forms as policies_forms

from openstack_dashboard import api as api_keystone
from openstack_dashboard.utils import identity


class CreateStaticPolicyView(forms.ModalFormView):
    form_class = policies_forms.CreateStaticPolicy
    form_id = "create_static_policy_form"

    modal_header = _("Create a Static Policy")
    modal_id = "create_static_policy_modal"
    submit_label = _("Create Policy")
    submit_url = reverse_lazy("horizon:crystal:policies:policies:create_static_policy")
    template_name = 'crystal/policies/policies/create_static_policy.html'
    content_object_name = 'policy'
    success_url = reverse_lazy('horizon:crystal:policies:index')
    page_title = _("Create a Static Policy")


class CreateDynamicPolicyView(forms.ModalFormView):
    form_class = policies_forms.CreateDynamicPolicy
    form_id = "create_dynamic_policy_form"

    modal_header = _("Create a Dynamic Policy")
    modal_id = "create_dynamic_policy_modal"
    submit_label = _("Create Dynamic Policy")
    submit_url = reverse_lazy("horizon:crystal:policies:policies:create_dynamic_policy")
    template_name = 'crystal/policies/policies/create_dynamic_policy.html'
    content_object_name = 'policy'
    success_url = reverse_lazy('horizon:crystal:policies:index')
    page_title = _("Create a Dynamic Policy")


@csrf_exempt
def get_container_by_project(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        if request.user.tenant_id == project_id:
            try:
                container_list = common.get_container_list(request)
                if len(container_list) > 0:
                    # If the project contains some containers
                    container_response = '<option value="">Select one</option>'
                    container_response += '<optgroup label="Containers">'
                    for container in container_list:
                        value, label = container
                        container_response += '<option value="' + str(value) + '">' + str(label) + '</option>'
                    container_response += '</optgroup>'
                else:
                    # If the project does not contain some containers
                    container_response = '<option value="">None</option>'
            except:
                # If get_container_list raises an exception
                container_response = '<option value="">None</option>'
        else:
            if project_id:
                # If the selected project is not the current project
                container_response = '<option value="">Not available</option>'
            else:
                # If the selected project is 'Select one'
                container_response = '<option value="">None</option>'

        # Generate response
        response = http.StreamingHttpResponse(container_response)
        return response


@csrf_exempt
def get_users_by_project(request):

    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        if request.user.tenant_id == project_id:

            try:
                domain_id = identity.get_domain_id_for_operation(request)
                users_list = [(user.id, user.name) for user in api_keystone.keystone.user_list(request, domain=domain_id, project=project_id)]
                    
                if len(users_list) > 0:
                    # If the project contains some containers
                    users_response = '<option value="">Select one</option>'
                    users_response += '<optgroup label="Users">'
                    for value, label in users_list:
                        users_response += '<option value="' + str(value) + '">' + str(label) + '</option>'

                else:
                    # If the project does not contain some containers
                    users_response = '<option value="">None</option>'
            except:
                # If get_container_list raises an exception
                users_response = '<option value="">None</option>'
        else:
            if project_id:
                # If the selected project is not the current project
                users_response = '<option value="">Not available</option>'
            else:
                # If the selected project is 'Select one'
                users_response = '<option value="">None</option>'

        # Generate response
        response = http.StreamingHttpResponse(users_response)
        return response
    


class CreateDSLPolicyView(forms.ModalFormView):
    form_class = policies_forms.CreateDSLPolicy
    form_id = "create_policy_dsl_form"

    modal_header = _("Create a Policy (DSL)")
    modal_id = "create_policy_dsl_modal"
    submit_label = _("Create")
    submit_url = reverse_lazy("horizon:crystal:policies:policies:create_dsl_policy")
    template_name = 'crystal/policies/policies/create_dsl_policy.html'
    content_object_name = 'policy'
    success_url = reverse_lazy('horizon:crystal:policies:index')
    page_title = _("Create a Policy (DSL)")


class UpdateStaticPolicyView(forms.ModalFormView):
    form_class = policies_forms.UpdatePolicy
    form_id = "update_static_policy_form"
    modal_header = _("Update a Policy (Simple)")
    submit_label = _("Update")
    submit_url = "horizon:crystal:policies:policies:update_static_policy"
    template_name = "crystal/policies/policies/update_static_policy.html"
    context_object_name = 'policy'
    success_url = reverse_lazy('horizon:crystal:policies:index')
    page_title = _("Update a Policy (Simple)")

    def get_context_data(self, **kwargs):
        context = super(UpdateStaticPolicyView, self).get_context_data(**kwargs)
        context['policy_id'] = self.kwargs['policy_id']
        args = (self.kwargs['policy_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        policy_id = self.kwargs['policy_id']
        try:
            policy = api.dsl_get_static_policy(self.request, policy_id)
            return policy
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve static policy details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        policy = self._get_object()
        initial = json.loads(policy.text)
        return initial


classes = ("ajax-modal",)
