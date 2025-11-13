from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.forms import ModelForm
from django import forms
from django.utils import timezone
from .models import Bus, DocumentoVehiculo, Mantenimiento


class BusForm(ModelForm):
    class Meta:
        model = Bus
        fields = ['placa', 'modelo', 'año_fabricacion', 'capacidad_pasajeros', 
                 'numero_chasis', 'numero_motor', 'estado', 'fecha_adquisicion']
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: ABC-1234'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Mercedes Benz O500RS'}),
            'año_fabricacion': forms.NumberInput(attrs={'class': 'form-control', 'min': 1990, 'max': 2030}),
            'capacidad_pasajeros': forms.NumberInput(attrs={'class': 'form-control', 'min': 10, 'max': 100}),
            'numero_chasis': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_motor': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'fecha_adquisicion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class BusListView(ListView):
    model = Bus
    template_name = 'flota/bus_list.html'
    context_object_name = 'buses'
    paginate_by = 20

    def get_queryset(self):
        return Bus.objects.all().order_by('-creado_en')


class BusDetailView(DetailView):
    model = Bus
    template_name = 'flota/bus_detail.html'
    context_object_name = 'bus'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context


class BusCreateView(CreateView):
    model = Bus
    form_class = BusForm
    template_name = 'flota/bus_form.html'
    success_url = reverse_lazy('bus_list')

    def form_valid(self, form):
        messages.success(self.request, f'Bus {form.instance.placa} creado exitosamente.')
        return super().form_valid(form)


class BusUpdateView(UpdateView):
    model = Bus
    form_class = BusForm
    template_name = 'flota/bus_form.html'
    success_url = reverse_lazy('bus_list')

    def form_valid(self, form):
        messages.success(self.request, f'Bus {form.instance.placa} actualizado exitosamente.')
        return super().form_valid(form)


class BusDeleteView(DeleteView):
    model = Bus
    template_name = 'flota/bus_confirm_delete.html'
    success_url = reverse_lazy('bus_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, f'Bus {self.object.placa} eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)
