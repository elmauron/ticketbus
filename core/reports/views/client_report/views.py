import json

from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import FormView

from core.cooperative.models import Client
from core.reports.forms import ReportForm
from core.security.mixins import GroupModuleMixin


class ClientReportView(GroupModuleMixin, FormView):
    template_name = 'client_report/report.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                term = request.POST['term']
                queryset = Client.objects.filter()
                if len(term):
                    queryset = queryset.filter(Q(user__names__icontains=term) | Q(user__dni__icontains=term))
                for i in queryset:
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Informe de Clientes'
        return context
