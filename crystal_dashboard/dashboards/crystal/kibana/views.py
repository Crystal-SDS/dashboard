from django.utils.translation import ugettext_lazy as _
from horizon import views
from django.conf import settings


class IndexView(views.APIView):
    # A very simple class-based view...
    template_name = 'crystal/kibana/index.html'
    page_title = _("Kibana")

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        context["kibana_host"] = request.META['HTTP_HOST'].split(':')[0]
        context["kibana_port"] = settings.KIBANA_PORT
        return context
