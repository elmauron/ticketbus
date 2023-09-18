import json

from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import TemplateView

from core.cooperative.models import Bus
from core.reports.forms import ReportForm
from core.security.mixins import GroupModuleMixin


class BusReportView(GroupModuleMixin, TemplateView):
    template_name = 'bus_report/report.html'

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                term = request.POST['term']
                member = request.POST['member']
                queryset = Bus.objects.filter()
                if len(member):
                    queryset = queryset.filter(member_id=member)
                if len(term):
                    queryset = queryset.filter(Q(name__icontains=term) | Q(plaque__icontains=term))
                for i in queryset:
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Informe de Buses'
        context['form'] = ReportForm()
        return context
