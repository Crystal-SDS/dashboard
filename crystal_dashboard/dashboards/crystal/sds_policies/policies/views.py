import json

from django import http
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from crystal_dashboard.api import crystal as api
from crystal_dashboard.dashboards.crystal import common
from crystal_dashboard.dashboards.crystal.sds_policies.policies import forms as policies_forms


class CreateSimplePolicyView(forms.ModalFormView):
    form_class = policies_forms.CreateSimplePolicy
    form_id = "create_simple_policy_form"

    modal_header = _("Create a Policy (Simple)")
    modal_id = "create_simple_policy_modal"
    submit_label = _("Create")
    submit_url = reverse_lazy("horizon:crystal:sds_policies:policies:create_simple_policy")
    template_name = 'crystal/sds_policies/policies/create_simple_policy.html'
    content_object_name = 'policy'
    success_url = reverse_lazy('horizon:crystal:sds_policies:index')
    page_title = _("Create a Policy (Simple)")


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
            except Exception as exc:
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


class CreateDSLPolicyView(forms.ModalFormView):
    form_class = policies_forms.CreateDSLPolicy
    form_id = "create_policy_dsl_form"

    modal_header = _("Create a Policy (DSL)")
    modal_id = "create_policy_dsl_modal"
    submit_label = _("Create")
    submit_url = reverse_lazy("horizon:crystal:sds_policies:policies:create_dsl_policy")
    template_name = 'crystal/sds_policies/policies/create_dsl_policy.html'
    content_object_name = 'policy'
    success_url = reverse_lazy('horizon:crystal:sds_policies:index')
    page_title = _("Create a Policy (DSL)")


class UpdateStaticPolicyView(forms.ModalFormView):
    form_class = policies_forms.UpdatePolicy
    form_id = "update_static_policy_form"
    modal_header = _("Update a Policy (Simple)")
    submit_label = _("Update")
    submit_url = "horizon:crystal:sds_policies:policies:update_static_policy"
    template_name = "crystal/sds_policies/policies/update_static_policy.html"
    context_object_name = 'policy'
    success_url = reverse_lazy('horizon:crystal:sds_policies:index')
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
