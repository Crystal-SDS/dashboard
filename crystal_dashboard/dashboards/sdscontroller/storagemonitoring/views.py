from django.conf import settings
from horizon import views


class IndexView(views.APIView):
    template_name = 'sdscontroller/storagemonitoring/system/_swift_project_plots.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        context["kibana_host"] = settings.KIBANA_HOST
        context["kibana_port"] = settings.KIBANA_PORT
        context["projects_plot"] = settings.IOSTACK_MONITORING_PROJECTS_PLOT
        return context


class SwiftContainerView(views.APIView):
    template_name = 'sdscontroller/storagemonitoring/system/_swift_container_plots.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        context["kibana_host"] = settings.KIBANA_HOST
        context["kibana_port"] = settings.KIBANA_PORT
        context["containers_plot"] = settings.IOSTACK_MONITORING_CONTAINERS_PLOT
        return context


class SystemView(views.APIView):
    template_name = 'sdscontroller/storagemonitoring/system/_system_plots.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        context["kibana_host"] = settings.KIBANA_HOST
        context["kibana_port"] = settings.KIBANA_PORT
        context["system_plot"] = settings.IOSTACK_MONITORING_SYSTEM_PLOT
        return context
