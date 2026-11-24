from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class RegistroAcceso(models.Model):
    class Motivo(models.TextChoices):
        VISITA = 'VISITA', 'Visita'
        DELIVERY = 'DELIVERY', 'Delivery'
        SERVICIO = 'SERVICIO', 'Servicio'
        OTRO = 'OTRO', 'Otro'

    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        AUTORIZADO = 'AUTORIZADO', 'Autorizado'
        RECHAZADO = 'RECHAZADO', 'Rechazado'
        FINALIZADO = 'FINALIZADO', 'Finalizado'

    # PROTECT: no se borra un visitante ni una vivienda que tengan historial de accesos
    visitante = models.ForeignKey(
        'accesos.Visitante', on_delete=models.PROTECT, related_name='accesos'
    )
    vivienda = models.ForeignKey(
        'accesos.Vivienda', on_delete=models.PROTECT, related_name='accesos'
    )
    # SET_NULL: si se borra el residente, el registro se conserva sin autorizador
    autorizado_por = models.ForeignKey(
        'accesos.Residente',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accesos_autorizados',
    )
    motivo = models.CharField(max_length=10, choices=Motivo.choices, default=Motivo.VISITA)
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.PENDIENTE)
    fecha_ingreso = models.DateTimeField(default=timezone.now)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    # Base de la regla de propiedad: solo quien lo creó podrá editarlo
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='registros_creados',
    )

    class Meta:
        ordering = ['-fecha_ingreso']
        verbose_name = 'registro de acceso'
        verbose_name_plural = 'registros de acceso'

    def __str__(self):
        return f'{self.visitante} -> {self.vivienda} ({self.get_estado_display()})'

    def get_absolute_url(self):
        return reverse('registro_detail', args=[self.pk])