from django import forms

from accesos.models import RegistroAcceso


class RegistroAccesoForm(forms.ModelForm):
    class Meta:
        model = RegistroAcceso
        # creado_por NO va aquí: lo asigna la vista con el usuario logueado
        fields = [
            'visitante', 'vivienda', 'autorizado_por',
            'motivo', 'estado', 'fecha_ingreso', 'fecha_salida',
        ]
        widgets = {
            # type="datetime-local" muestra un selector de fecha y hora en el navegador
            'fecha_ingreso': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'
            ),
            'fecha_salida': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'
            ),
        }

    # Validación propia que compara dos campos entre sí
    def clean(self):
        datos = super().clean()
        ingreso = datos.get('fecha_ingreso')
        salida = datos.get('fecha_salida')
        if ingreso and salida and salida < ingreso:
            self.add_error('fecha_salida', 'La salida no puede ser anterior al ingreso.')
        return datos