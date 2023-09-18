import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.cooperative.forms import Bus, BusForm
from core.security.mixins import GroupPermissionMixin


class BusListView(GroupPermissionMixin, ListView):
    model = Bus
    template_name = 'bus/list.html'
    permission_required = 'view_bus'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Bus.objects.filter():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Buses'
        context['create_url'] = reverse_lazy('bus_create')
        return context


class BusCreateView(GroupPermissionMixin, CreateView):
    model = Bus
    template_name = 'bus/create.html'
    form_class = BusForm
    success_url = reverse_lazy('bus_list')
    permission_required = 'add_bus'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Bus.objects.all()
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'plaque':
                    data['valid'] = not queryset.filter(plaque__iexact=parameter).exists()
                elif pattern == 'car_disk':
                    data['valid'] = not queryset.filter(car_disk=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Bus'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class BusUpdateView(GroupPermissionMixin, UpdateView):
    model = Bus
    template_name = 'bus/create.html'
    form_class = BusForm
    success_url = reverse_lazy('bus_list')
    permission_required = 'change_bus'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Bus.objects.all().exclude(id=self.object.id)
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'plaque':
                    data['valid'] = not queryset.filter(plaque__iexact=parameter).exists()
                elif pattern == 'car_disk':
                    data['valid'] = not queryset.filter(car_disk=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de un Bus'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class BusDeleteView(GroupPermissionMixin, DeleteView):
    model = Bus
    template_name = 'delete.html'
    success_url = reverse_lazy('bus_list')
    permission_required = 'delete_bus'

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
