from django.conf import settings
from horizon import views


class IndexView(views.APIView):
    template_name = 'crystal/analytics_monitoring/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        context["spark_dashboard_url"] = settings.SPARK_DASHBOARD_URL
        return context


class HistoryServerView(views.APIView):
    template_name = 'crystal/analytics_monitoring/history_server.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        context["spark_history_server_url"] = settings.SPARK_HISTORY_SERVER_URL
        return context


class FlinkDashboardView(views.APIView):
    template_name = 'crystal/analytics_monitoring/flink_dashboard.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        context["flink_dashboard_url"] = settings.FLINK_DASHBOARD_URL
        return context
