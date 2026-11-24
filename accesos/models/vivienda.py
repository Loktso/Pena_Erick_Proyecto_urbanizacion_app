from django.db import models
from django.urls import reverse


class Vivienda(models.Model):
    # Opciones cerradas para el tipo de vivienda
    class Tipo(models.TextChoices):
        CASA = 'CASA', 'Casa'
        DEPARTAMENTO = 'DEPTO', 'Departamento'

    manzana = models.CharField(max_length=10)
    numero = models.CharField(max_length=10)
    tipo = models.CharField(max_length=10, choices=Tipo.choices, default=Tipo.CASA)
    fecha_registro = models.DateField(auto_now_add=True)  # se llena sola al crear

    class Meta:
        ordering = ['manzana', 'numero']
        verbose_name = 'vivienda'
        verbose_name_plural = 'viviendas'
        # No puede haber dos viviendas con la misma manzana y número
        constraints = [
            models.UniqueConstraint(fields=['manzana', 'numero'], name='vivienda_unica')
        ]

    def __str__(self):
        return f'Mz {self.manzana} - {self.get_tipo_display()} {self.numero}'

    def get_absolute_url(self):
        return reverse('vivienda_detail', args=[self.pk])