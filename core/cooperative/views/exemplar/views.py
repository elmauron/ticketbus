import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.cooperative.forms import Exemplar, ExemplarForm
from core.security.mixins import GroupPermissionMixin


class ExemplarListView(GroupPermissionMixin, TemplateView):
    template_name = 'exemplar/list.html'
    permission_required = 'view_exemplar'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Exemplar.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Modelos'
        context['create_url'] = reverse_lazy('exemplar_create')
        return context


class ExemplarCreateView(GroupPermissionMixin, CreateView):
    model = Exemplar
    template_name = 'exemplar/create.html'
    form_class = ExemplarForm
    success_url = reverse_lazy('exemplar_list')
    permission_required = 'add_exemplar'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Exemplar.objects.all()
                name = request.POST['name'].strip()
                brand = request.POST['brand']
                if len(brand):
                    data['valid'] = not queryset.filter(name__iexact=name, brand_id=brand).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Modelo'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ExemplarUpdateView(GroupPermissionMixin, UpdateView):
    model = Exemplar
    template_name = 'exemplar/create.html'
    form_class = ExemplarForm
    success_url = reverse_lazy('exemplar_list')
    permission_required = 'change_exemplar'

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
                queryset = Exemplar.objects.all().exclude(id=self.object.id)
                name = request.POST['name'].strip()
                brand = request.POST['brand']
                if len(brand):
                    data['valid'] = not queryset.filter(name__iexact=name, brand_id=brand).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de una Módelo'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ExemplarDeleteView(GroupPermissionMixin, DeleteView):
    model = Exemplar
    template_name = 'delete.html'
    success_url = reverse_lazy('exemplar_list')
    permission_required = 'delete_exemplar'

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
