from django.db import models
from core.models import Conductor, Lugar
from flota.models import Bus


class Viaje(models.Model):
    """
    Modelo para registrar viajes planificados de la flota.
    """
    ESTADO_VIAJE = [
        ('programado', 'Programado'),
        ('en_curso', 'En Curso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT, related_name='viajes')
    conductor = models.ForeignKey(Conductor, on_delete=models.PROTECT, related_name='viajes')
    lugar_origen = models.ForeignKey(Lugar, on_delete=models.PROTECT, related_name='viajes_origen')
    lugar_destino = models.ForeignKey(Lugar, on_delete=models.PROTECT, related_name='viajes_destino')
    fecha_salida = models.DateTimeField()
    fecha_llegada_estimada = models.DateTimeField()
    fecha_llegada_real = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_VIAJE, default='programado')
    latitud_origen = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud_origen = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitud_destino = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud_destino = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    pasajeros_confirmados = models.IntegerField(default=0)
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_salida']
        verbose_name = 'Viaje'
        verbose_name_plural = 'Viajes'

    def __str__(self):
        return f"{self.bus.placa} - {self.lugar_origen.nombre} -> {self.lugar_destino.nombre} ({self.fecha_salida.date()})"
