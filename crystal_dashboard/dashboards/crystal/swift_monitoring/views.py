from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from horizon import views


class CrystalDashboard(views.APIView):
    template_name = 'crystal/swift_monitoring/system/_crystal_swift_overview.html'
    page_title = _("Swift Cluster")

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        context["kibana_host"] = request.META['HTTP_HOST'].split(':')[0]
        context["kibana_port"] = settings.KIBANA_PORT
        context["crystal_dashboard"] = settings.CRYSTAL_MONITORING_DASHBOARD
        return context
