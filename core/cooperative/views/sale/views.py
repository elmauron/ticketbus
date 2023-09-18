import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView
from django.views.generic.base import View

from config import settings
from core.cooperative import printer
from core.cooperative.choices import PAYMENT_CONDITION, PAYMENT_METHOD, VOUCHER
from core.cooperative.forms import SaleForm, ClientForm, ClientUserForm, Sale, Company, SaleDetail, Client, Bus, Route
from core.reports.forms import ReportForm
from core.security.mixins import GroupPermissionMixin


class SaleListView(GroupPermissionMixin, FormView):
    template_name = 'sale/admin/list.html'
    permission_required = 'view_sale'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Sale.objects.filter()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset.order_by('-id'):
                    data.append(i.toJSON())
            elif action == 'search_detail_tickets':
                data = []
                for i in SaleDetail.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('sale_create')
        return context


class SaleCreateView(GroupPermissionMixin, CreateView):
    model = Sale
    template_name = 'sale/admin/create.html'
    form_class = SaleForm
    success_url = reverse_lazy('sale_list')
    permission_required = 'add_sale'

    def get_form(self, form_class=None):
        form = SaleForm()
        client = Client.objects.filter(dni='9999999999999')
        if client.exists():
            client = client[0]
            form.fields['client'].queryset = Client.objects.filter(id=client.id)
            form.initial = {'client': client}
        return form

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    sale = Sale()
                    sale.employee_id = request.user.id
                    sale.client_id = int(request.POST['client'])
                    sale.payment_method = request.POST['payment_method']
                    sale.type_voucher = request.POST['type_voucher']
                    sale.iva = float(Company.objects.first().iva) / 100
                    sale.save()
                    for i in json.loads(request.POST['tickets']):
                        saledetail = SaleDetail()
                        saledetail.sale_id = sale.id
                        saledetail.route_id = int(i['route']['id'])
                        saledetail.price = float(i['route']['price'])
                        saledetail.cant = 1
                        saledetail.seat = int(i['seat'])
                        saledetail.subtotal = saledetail.price * saledetail.cant
                        saledetail.save()
                    sale.calculate_invoice()
                    if sale.payment_condition == PAYMENT_CONDITION[0][0]:
                        if sale.payment_method == PAYMENT_METHOD[0][0]:
                            sale.cash = float(request.POST['cash'])
                            sale.change = float(sale.cash) - sale.total
                            sale.save()
                        elif sale.payment_method == PAYMENT_METHOD[1][0]:
                            sale.card_number = request.POST['card_number']
                            sale.card_titular = request.POST['card_titular']
                            sale.card_amount_debited = float(request.POST['card_amount_debited'])
                            sale.card_type = request.POST['card_type']
                            sale.card_year = request.POST['card_year']
                            sale.card_code_verification = request.POST['card_code_verification']
                            sale.save()
                        elif sale.payment_method == PAYMENT_METHOD[2][0]:
                            sale.cash = float(request.POST['cash'])
                            sale.card_number = request.POST['card_number']
                            sale.titular = request.POST['card_titular']
                            sale.amount_debited = float(request.POST['card_amount_debited'])
                            sale.save()
                    sale.send_data_with_socket()
                    print_url = reverse_lazy('sale_print_invoice', kwargs={'pk': sale.id})
                    data = {'print_url': str(print_url)}
            elif action == 'search_bus_by_place':
                data = [{'id': '', 'text': '-------------'}]
                place = request.POST['place']
                if len(place):
                    buses = Bus.objects.filter(route__place_id=place).distinct()
                    for i in buses:
                        item = i.toJSON()
                        item['text'] = f'{i.name} (Anden:{i.car_disk})'
                        data.append(item)
            elif action == 'search_route_by_bus':
                data = [{'id': '', 'text': '-------------'}]
                bus = request.POST['bus']
                place = request.POST['place']
                if len(bus) and len(place):
                    current_hour = datetime.now().time()
                    queryset = Route.objects.filter(place_id=place, bus_id=bus).exclude(state=False).order_by('departure_time')
                    for i in queryset:
                        if current_hour <= i.departure_time:
                            item = i.toJSON()
                            item['text'] = f'H.Salida: {i.departure_time_format()} / Precio: ${i.price:.2f}'
                            item['occupied'] = i.search_seats()
                            data.append(item)
            elif action == 'search_client':
                data = []
                term = request.POST['term']
                for i in Client.objects.filter(Q(user__names__icontains=term) | Q(dni__icontains=term)).order_by('user__names')[0:10]:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'validate_client':
                data = {'valid': True}
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                queryset = Client.objects.all()
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(dni=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(user__email=parameter).exists()
            elif action == 'create_client':
                with transaction.atomic():
                    form1 = ClientUserForm(self.request.POST, self.request.FILES)
                    form2 = ClientForm(request.POST)
                    if form1.is_valid() and form2.is_valid():
                        user = form1.save(commit=False)
                        user.username = form2.cleaned_data.get('dni')
                        user.set_password(user.username)
                        user.save()
                        user.groups.add(Group.objects.get(pk=settings.GROUPS.get('client')))
                        form_client = form2.save(commit=False)
                        form_client.user = user
                        form_client.save()
                        data = Client.objects.get(pk=form_client.id).toJSON()
                    else:
                        if not form1.is_valid():
                            data['error'] = form1.errors
                        elif not form2.is_valid():
                            data['error'] = form2.errors
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_socket_url(self):
        URL = self.request.build_absolute_uri('/').strip('/').split(':')
        return f'{URL[0]}:{URL[1]}:{settings.SOCKET_PORT}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de una Venta'
        context['frmClient'] = ClientForm()
        context['frmUser'] = ClientUserForm()
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['socket_url'] = self.get_socket_url()
        return context


class SaleDeleteView(GroupPermissionMixin, DeleteView):
    model = Sale
    template_name = 'delete.html'
    success_url = reverse_lazy('sale_list')
    permission_required = 'delete_sale'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context


class SaleClientListView(GroupPermissionMixin, FormView):
    template_name = 'sale/client/list.html'
    form_class = ReportForm
    permission_required = 'view_client_sale'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Sale.objects.filter(client__user_id=request.user.id)
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset.order_by('-id'):
                    data.append(i.toJSON())
            elif action == 'search_detail_tickets':
                data = []
                for i in SaleDetail.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Boletos'
        context['create_url'] = reverse_lazy('sale_client_create')
        return context


class SaleClientCreateView(GroupPermissionMixin, CreateView):
    model = Sale
    template_name = 'sale/client/create.html'
    form_class = SaleForm
    success_url = reverse_lazy('sale_client_list')
    permission_required = 'add_client_sale'

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    sale = Sale()
                    sale.employee_id = request.user.id
                    sale.client_id = request.user.client.id
                    sale.payment_method = 'tarjeta_debito_credito'
                    sale.type_voucher = request.POST['type_voucher']
                    sale.iva = float(Company.objects.first().iva) / 100
                    sale.save()
                    for i in json.loads(request.POST['tickets']):
                        saledetail = SaleDetail()
                        saledetail.sale_id = sale.id
                        saledetail.route_id = int(i['route']['id'])
                        saledetail.price = float(i['route']['price'])
                        saledetail.cant = 1
                        saledetail.seat = int(i['seat'])
                        saledetail.subtotal = saledetail.price * saledetail.cant
                        saledetail.save()
                    sale.calculate_invoice()
                    if sale.payment_method == PAYMENT_METHOD[1][0]:
                        sale.card_number = request.POST['card_number']
                        sale.card_titular = request.POST['card_titular']
                        sale.card_amount_debited = sale.total
                        sale.card_type = request.POST['card_type']
                        sale.card_year = request.POST['card_year']
                        sale.card_code_verification = request.POST['card_code_verification']
                        sale.save()
                    sale.send_data_with_socket()
                    print_url = reverse_lazy('sale_print_invoice', kwargs={'pk': sale.id})
                    data = {'print_url': str(print_url)}
            elif action == 'search_bus_by_place':
                data = [{'id': '', 'text': '-------------'}]
                place = request.POST['place']
                if len(place):
                    buses = Bus.objects.filter(route__place_id=place).distinct()
                    for i in buses:
                        item = i.toJSON()
                        item['text'] = f'{i.name} (Anden:{i.car_disk})'
                        data.append(item)
            elif action == 'search_route_by_bus':
                data = [{'id': '', 'text': '-------------'}]
                bus = request.POST['bus']
                place = request.POST['place']
                if len(bus) and len(place):
                    current_hour = datetime.now().time()
                    queryset = Route.objects.filter(place_id=place, bus_id=bus).exclude(state=False).order_by('departure_time')
                    for i in queryset:
                        if current_hour <= i.departure_time:
                            item = i.toJSON()
                            item['text'] = f'H.Salida: {i.departure_time_format()} / Precio: ${i.price:.2f}'
                            item['occupied'] = i.search_seats()
                            data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_socker_url(self):
        URL = self.request.build_absolute_uri('/').strip('/').split(':')
        return f'{URL[0]}:{URL[1]}:{settings.SOCKET_PORT}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Compra de Boletos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['socket_url'] = self.get_socker_url()
        return context


class SalePrintInvoiceView(LoginRequiredMixin, View):
    success_url = reverse_lazy('sale_admin_list')

    def get_success_url(self):
        if self.request.user.is_client():
            return reverse_lazy('sale_client_list')
        return self.success_url

    def get_object(self):
        queryset = Sale.objects.filter(id=self.kwargs['pk'])
        if queryset.exists():
            return queryset[0]
        return None

    def get(self, request, *args, **kwargs):
        try:
            sale = self.get_object()
            if sale is not None:
                context = {'sale': sale, 'company': Company.objects.first(), 'height': 450 + sale.saledetail_set.all().count() * 10}
                if sale.type_voucher == VOUCHER[0][0]:
                    pdf_file = printer.create_pdf(context=context, template_name='sale/format/ticket.html')
                else:
                    pdf_file = printer.create_pdf(context=context, template_name='sale/format/invoice.html')
                return HttpResponse(pdf_file, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(self.get_success_url())
