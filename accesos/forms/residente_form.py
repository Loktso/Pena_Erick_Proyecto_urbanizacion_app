from django import forms

from accesos.models import Residente


class ResidenteForm(forms.ModelForm):
    class Meta:
        model = Residente
        fields = ['nombres', 'apellidos', 'cedula', 'telefono', 'email', 'viviendas']
        widgets = {
            'cedula': forms.TextInput(attrs={'placeholder': '10 dígitos', 'maxlength': '10'}),
            'viviendas': forms.CheckboxSelectMultiple(),  # casillas para el ManyToMany
        }

    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        if not cedula.isdigit() or len(cedula) != 10:
            raise forms.ValidationError('La cédula debe tener exactamente 10 dígitos.')
        return cedula