import json

from django.http import HttpResponse
from django.views.generic import TemplateView

from core.cooperative.models import Route
from core.reports.forms import ReportForm
from core.security.mixins import GroupModuleMixin


class RouteReportView(GroupModuleMixin, TemplateView):
    template_name = 'route_report/report.html'

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                place = request.POST['place']
                bus = request.POST['bus']
                chauffeur = request.POST['chauffeur']
                queryset = Route.objects.filter()
                if len(bus):
                    queryset = queryset.filter(bus_id=bus)
                if len(chauffeur):
                    queryset = queryset.filter(chauffeur_id=chauffeur)
                if len(place):
                    queryset = queryset.filter(place__id=place)
                for i in queryset:
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Informe de Rutas'
        context['form'] = ReportForm()
        return context
