from django.db import models


class Conductor(models.Model):
    """
    Modelo para registrar conductores de la flota.
    """
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    fecha_contratacion = models.DateField()
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['apellido', 'nombre']
        verbose_name = 'Conductor'
        verbose_name_plural = 'Conductores'

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


class Lugar(models.Model):
    """
    Modelo para registrar lugares (origen, destino, paradas).
    """
    nombre = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100, blank=True)
    pais = models.CharField(max_length=100, default='Ecuador')
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ciudad', 'nombre']
        verbose_name = 'Lugar'
        verbose_name_plural = 'Lugares'

    def __str__(self):
        return f"{self.nombre}, {self.ciudad}"
