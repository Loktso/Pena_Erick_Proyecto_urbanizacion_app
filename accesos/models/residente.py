from django.db import models
from django.urls import reverse


class Residente(models.Model):
    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    cedula = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    # Un residente puede vivir en varias viviendas y una vivienda tiene varios residentes
    viviendas = models.ManyToManyField(
        'accesos.Vivienda', related_name='residentes', blank=True
    )

    class Meta:
        ordering = ['apellidos', 'nombres']
        verbose_name = 'residente'
        verbose_name_plural = 'residentes'

    def __str__(self):
        return f'{self.apellidos} {self.nombres}'

    def get_absolute_url(self):
        return reverse('residente_detail', args=[self.pk])