from django.db import models


class Bus(models.Model):
    """
    Modelo para registrar buses de la flota.
    """
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('mantenimiento', 'En Mantenimiento'),
        ('inactivo', 'Inactivo'),
    ]
    
    placa = models.CharField(max_length=20, unique=True)
    modelo = models.CharField(max_length=100)
    año_fabricacion = models.IntegerField()
    capacidad_pasajeros = models.IntegerField()
    numero_chasis = models.CharField(max_length=30, unique=True)
    numero_motor = models.CharField(max_length=30, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    fecha_adquisicion = models.DateField()
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['placa']
        verbose_name = 'Bus'
        verbose_name_plural = 'Buses'

    def __str__(self):
        return f"{self.placa} - {self.modelo}"


class DocumentoVehiculo(models.Model):
    """
    Modelo para registrar documentos del vehículo (SOAT, REC, etc).
    """
    TIPO_DOCUMENTO = [
        ('soat', 'SOAT'),
        ('rec', 'REC'),
        ('matricula', 'Matrícula'),
        ('revision', 'Revisión Técnica'),
        ('otro', 'Otro'),
    ]
    
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='documentos')
    tipo = models.CharField(max_length=20, choices=TIPO_DOCUMENTO)
    numero_documento = models.CharField(max_length=50)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    archivo = models.FileField(upload_to='documentos_vehiculos/', blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_vencimiento']
        verbose_name = 'Documento Vehículo'
        verbose_name_plural = 'Documentos Vehículos'

    def __str__(self):
        return f"{self.bus.placa} - {self.get_tipo_display()}"


class Mantenimiento(models.Model):
    """
    Modelo para registrar mantenimientos realizados en los buses.
    """
    TIPO_MANTENIMIENTO = [
        ('preventivo', 'Preventivo'),
        ('correctivo', 'Correctivo'),
        ('mecanico', 'Mecánico'),
        ('electrico', 'Eléctrico'),
        ('otro', 'Otro'),
    ]
    
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='mantenimientos')
    tipo = models.CharField(max_length=20, choices=TIPO_MANTENIMIENTO)
    descripcion = models.TextField()
    fecha_mantenimiento = models.DateField()
    kilometraje = models.IntegerField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    taller = models.CharField(max_length=150, blank=True)
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_mantenimiento']
        verbose_name = 'Mantenimiento'
        verbose_name_plural = 'Mantenimientos'

    def __str__(self):
        return f"{self.bus.placa} - {self.get_tipo_display()} ({self.fecha_mantenimiento})"
