import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.cooperative.forms import Brand, BrandForm
from core.security.mixins import GroupPermissionMixin


class BrandListView(GroupPermissionMixin, TemplateView):
    template_name = 'brand/list.html'
    permission_required = 'view_brand'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Brand.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Marcas'
        context['create_url'] = reverse_lazy('brand_create')
        return context


class BrandCreateView(GroupPermissionMixin, CreateView):
    model = Brand
    template_name = 'brand/create.html'
    form_class = BrandForm
    success_url = reverse_lazy('brand_list')
    permission_required = 'add_brand'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Brand.objects.all()
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'name':
                    data['valid'] = not queryset.filter(name__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de una Marca'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class BrandUpdateView(GroupPermissionMixin, UpdateView):
    model = Brand
    template_name = 'brand/create.html'
    form_class = BrandForm
    success_url = reverse_lazy('brand_list')
    permission_required = 'change_brand'

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
                queryset = Brand.objects.all().exclude(id=self.object.id)
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'name':
                    data['valid'] = not queryset.filter(name__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de una Marca'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class BrandDeleteView(GroupPermissionMixin, DeleteView):
    model = Brand
    template_name = 'delete.html'
    success_url = reverse_lazy('brand_list')
    permission_required = 'delete_brand'

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
