from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


from crystal_dashboard.api import controllers as api
import json

from horizon import exceptions
from horizon import forms
from horizon import workflows

from crystal_dashboard.dashboards.crystal.projects.groups import workflows as project_workflows



class CreateGroupView(workflows.WorkflowView):
    workflow_class = project_workflows.CreateGroup

    def get_initial(self):
        initial = super(CreateGroupView, self).get_initial()
        return initial