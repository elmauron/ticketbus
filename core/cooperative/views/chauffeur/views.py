import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from core.cooperative.forms import ChauffeurForm, Chauffeur
from core.security.mixins import GroupPermissionMixin


class ChauffeurListView(GroupPermissionMixin, TemplateView):
    template_name = 'chauffeur/list.html'
    permission_required = 'view_chauffeur'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Chauffeur.objects.filter():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Choferes'
        context['create_url'] = reverse_lazy('chauffeur_create')
        return context


class ChauffeurCreateView(GroupPermissionMixin, CreateView):
    model = Chauffeur
    template_name = 'chauffeur/create.html'
    form_class = ChauffeurForm
    success_url = reverse_lazy('chauffeur_list')
    permission_required = 'add_chauffeur'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Chauffeur.objects.all()
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(dni=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(email=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Chofer'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ChauffeurUpdateView(GroupPermissionMixin, UpdateView):
    model = Chauffeur
    template_name = 'chauffeur/create.html'
    form_class = ChauffeurForm
    success_url = reverse_lazy('chauffeur_list')
    permission_required = 'change_chauffeur'

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
                queryset = Chauffeur.objects.all().exclude(id=self.object.id)
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(dni=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(email=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de un Chofer'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ChauffeurDeleteView(GroupPermissionMixin, DeleteView):
    model = Chauffeur
    template_name = 'delete.html'
    success_url = reverse_lazy('chauffeur_list')
    permission_required = 'delete_chauffeur'

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
