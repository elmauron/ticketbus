import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from core.cooperative.forms import Route, RouteForm, Bus
from core.security.mixins import GroupPermissionMixin


class RouteListView(GroupPermissionMixin, ListView):
    model = Route
    template_name = 'route/admin/list.html'
    permission_required = 'view_route'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Route.objects.filter():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Rutas'
        context['create_url'] = reverse_lazy('route_create')
        return context


class RouteCreateView(GroupPermissionMixin, CreateView):
    model = Route
    template_name = 'route/admin/create.html'
    form_class = RouteForm
    success_url = reverse_lazy('route_list')
    permission_required = 'add_route'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'search_bus_id':
                data = Bus.objects.get(pk=request.POST['id']).toJSON()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de una Ruta'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class RouteUpdateView(GroupPermissionMixin, UpdateView):
    model = Route
    template_name = 'route/admin/create.html'
    form_class = RouteForm
    success_url = reverse_lazy('route_list')
    permission_required = 'change_route'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'search_bus_id':
                data = Bus.objects.get(pk=request.POST['id']).toJSON()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de una Ruta'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class RouteDeleteView(GroupPermissionMixin, DeleteView):
    model = Route
    template_name = 'delete.html'
    success_url = reverse_lazy('route_list')
    permission_required = 'delete_route'

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


class RouteClientListView(GroupPermissionMixin, TemplateView):
    template_name = 'route/client/list.html'
    permission_required = 'view_client_route'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Route.objects.filter(state=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Rutas'
        return context
