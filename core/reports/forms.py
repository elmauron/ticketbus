from django import forms

from core.cooperative.models import *


class ReportForm(forms.Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Buscar por rangos de fecha')

    member = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;',
    }), queryset=Member.objects.all(), label='Socio')

    place = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;',
    }), queryset=Place.objects.all(), label='Destino')

    bus = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;',
    }), queryset=Bus.objects.all(), label='Bus')

    client = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;',
    }), queryset=Client.objects.all(), label='Cliente')

    chauffeur = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;',
    }), queryset=Chauffeur.objects.all(), label='Chofer')

    search = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese una descripción',
        'autocomplete': 'off'
    }), label='Buscador')
