from django.conf import settings
from django.db import models
from django.urls import reverse


class Visitante(models.Model):
    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    cedula = models.CharField(max_length=10, unique=True)
    placa = models.CharField(max_length=10, blank=True)  # solo si llega en vehículo
    # PROTECT: no se puede borrar un usuario que ya registró visitantes
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='visitantes_creados',
    )

    class Meta:
        ordering = ['apellidos', 'nombres']
        verbose_name = 'visitante'
        verbose_name_plural = 'visitantes'

    def __str__(self):
        return f'{self.apellidos} {self.nombres}'

    def get_absolute_url(self):
        return reverse('visitante_detail', args=[self.pk])