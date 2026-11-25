from django import forms

from accesos.models import Visitante


class VisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        # creado_por NO va aquí: lo asigna la vista con el usuario logueado
        fields = ['nombres', 'apellidos', 'cedula', 'placa']
        widgets = {
            'nombres': forms.TextInput(attrs={'placeholder': 'Nombres'}),
            'apellidos': forms.TextInput(attrs={'placeholder': 'Apellidos'}),
            'cedula': forms.TextInput(attrs={'placeholder': '10 dígitos', 'maxlength': '10'}),
            'placa': forms.TextInput(attrs={'placeholder': 'Solo si llega en vehículo'}),
        }

    # Validación propia: se ejecuta automáticamente para el campo "cedula"
    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        if not cedula.isdigit() or len(cedula) != 10:
            raise forms.ValidationError('La cédula debe tener exactamente 10 dígitos.')
        return cedula

    # Convierte la placa a mayúsculas antes de guardarla
    def clean_placa(self):
        return self.cleaned_data['placa'].upper()