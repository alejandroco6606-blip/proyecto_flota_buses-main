from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.forms import ModelForm
from django import forms
from django.utils import timezone
from .models import Viaje
from core.models import Conductor, Lugar
from flota.models import Bus


class ViajeForm(ModelForm):
    class Meta:
        model = Viaje
        fields = [
            'bus', 'conductor', 'lugar_origen', 'lugar_destino',
            'fecha_salida', 'fecha_llegada_estimada', 'fecha_llegada_real',
            'estado', 'pasajeros_confirmados', 'observaciones'
        ]
        widgets = {
            'bus': forms.Select(attrs={'class': 'form-control'}),
            'conductor': forms.Select(attrs={'class': 'form-control'}),
            'lugar_origen': forms.Select(attrs={'class': 'form-control'}),
            'lugar_destino': forms.Select(attrs={'class': 'form-control'}),
            'fecha_salida': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Fecha y hora de salida'
            }),
            'fecha_llegada_estimada': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Fecha y hora estimada de llegada'
            }),
            'fecha_llegada_real': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Fecha y hora real de llegada (opcional)'
            }),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'pasajeros_confirmados': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Número de pasajeros confirmados'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales (opcional)'
            }),
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Capturar coordenadas del lugar de origen
        if instance.lugar_origen:
            instance.latitud_origen = instance.lugar_origen.latitud
            instance.longitud_origen = instance.lugar_origen.longitud
        # Capturar coordenadas del lugar de destino
        if instance.lugar_destino:
            instance.latitud_destino = instance.lugar_destino.latitud
            instance.longitud_destino = instance.lugar_destino.longitud
        if commit:
            instance.save()
        return instance


# Vistas para Viajes
class ViajeListView(ListView):
    model = Viaje
    template_name = 'viajes/viaje_list.html'
    context_object_name = 'viajes'
    paginate_by = 20

    def get_queryset(self):
        return Viaje.objects.all().order_by('-fecha_salida')


class ViajeDetailView(DetailView):
    model = Viaje
    template_name = 'viajes/viaje_detail.html'
    context_object_name = 'viaje'


class ViajeCreateView(CreateView):
    model = Viaje
    form_class = ViajeForm
    template_name = 'viajes/viaje_form.html'
    success_url = reverse_lazy('viajes:viaje_list')

    def form_valid(self, form):
        messages.success(
            self.request,
            f'Viaje {form.instance.bus.placa} creado exitosamente.'
        )
        return super().form_valid(form)


class ViajeUpdateView(UpdateView):
    model = Viaje
    form_class = ViajeForm
    template_name = 'viajes/viaje_form.html'
    success_url = reverse_lazy('viajes:viaje_list')

    def form_valid(self, form):
        messages.success(
            self.request,
            f'Viaje {form.instance.bus.placa} actualizado exitosamente.'
        )
        return super().form_valid(form)


class ViajeDeleteView(DeleteView):
    model = Viaje
    template_name = 'viajes/viaje_confirm_delete.html'
    success_url = reverse_lazy('viajes:viaje_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(
            request,
            f'Viaje {self.object.bus.placa} eliminado exitosamente.'
        )
        return super().delete(request, *args, **kwargs)
