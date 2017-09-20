from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import forms

from crystal_dashboard.dashboards.sdscontroller.analytics_jobs.jobs import forms as jobs_forms


class SubmitJobView(forms.ModalFormView):
    form_class = jobs_forms.SubmitJob
    modal_header = _("Submit Job")
    modal_id = "submit_job_modal"
    template_name = 'sdscontroller/analytics_jobs/jobs/create.html'
    success_url = reverse_lazy('horizon:sdscontroller:analytics_jobs:index')
    page_title = _("Submit a Job")
    submit_label = _("Submit")
    submit_url = reverse_lazy(
        "horizon:sdscontroller:analytics_jobs:jobs:submit_job")