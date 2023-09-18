import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.views.generic import TemplateView

from core.cooperative.models import Sale, SaleDetail, Bus, Category, Route, Client
from core.reports.choices import MONTHS
from core.security.models import Dashboard


class DashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        dashboard = Dashboard.objects.filter()
        if dashboard.exists():
            if dashboard[0].layout == 1:
                return 'vtc_dashboard.html'
        return 'hzt_dashboard.html'

    def get(self, request, *args, **kwargs):
        request.user.set_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'get_graph_tickets_by_bus':
                data = []
                current_date = datetime.now().date()
                ids = list(SaleDetail.objects.filter(date_joined__year=current_date.year, date_joined__month=current_date.month).values_list('route__bus_id', flat=True).order_by('route__bus_id').distinct())
                for i in Bus.objects.filter(id__in=ids):
                    cant = SaleDetail.objects.filter(route__bus=i, date_joined__year=current_date.year, date_joined__month=current_date.month).count()
                    data.append([i.name, cant])
            elif action == 'get_graph_sale':
                data = []
                year = datetime.now().year
                for i in MONTHS[1:]:
                    result = Sale.objects.filter(date_joined__month=i[0], date_joined__year=year).aggregate(
                        result=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('result')
                    data.append(float(result))
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        if not self.request.user.is_client():
            context['clients'] = Client.objects.all().count()
            context['buses'] = Bus.objects.all().count()
            context['categories'] = Category.objects.filter().count()
            context['routes'] = Route.objects.all().count()
            context['sales'] = Sale.objects.filter().order_by('-id')[0:10]
            context['month'] = MONTHS[datetime.now().month][1]
        return context
