from django.urls import path

from core.reports.views.bus_report.views import BusReportView
from core.reports.views.client_report.views import ClientReportView
from core.reports.views.route_report.views import RouteReportView
from core.reports.views.sale_report.views import SaleReportView

urlpatterns = [
    path('bus/', BusReportView.as_view(), name='bus_report'),
    path('route/', RouteReportView.as_view(), name='route_report'),
    path('sale/', SaleReportView.as_view(), name='sale_report'),
    path('client/', ClientReportView.as_view(), name='client_report'),
]
