from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from horizon import exceptions
from horizon import forms
from horizon import workflows
import json

from crystal_dashboard.api import projects as api
from crystal_dashboard.dashboards.crystal.projects.groups import workflows as project_workflows


class CreateGroupView(workflows.WorkflowView):
    workflow_class = project_workflows.CreateGroup

    def get_initial(self):
        initial = super(CreateGroupView, self).get_initial()
        return initial
    
    
class UpdateGroupView(workflows.WorkflowView):
    workflow_class = project_workflows.UpdateGroup

    def get_context_data(self, **kwargs):
        context = super(UpdateGroupView, self).get_context_data(**kwargs)
        context["id"] = self.kwargs['id']
        return context

    def get_object(self, *args, **kwargs):
        group_id = self.kwargs['id']
        try:
            group = json.loads(api.get_project_group(self.request, group_id).text)
            group['group_id'] = group_id
        except Exception:
            redirect = reverse("horizon:crystal:projects:index")
            msg = _('Unable to retrieve group details.')
            exceptions.handle(self.request, msg, redirect=redirect)
        return group

    def get_initial(self):
        initial = super(UpdateGroupView, self).get_initial()
        group = self.get_object()
        return group
