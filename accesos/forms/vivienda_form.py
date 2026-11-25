from django import forms

from accesos.models import Vivienda


class ViviendaForm(forms.ModelForm):
    class Meta:
        model = Vivienda
        fields = ['manzana', 'numero', 'tipo']
        widgets = {
            'manzana': forms.TextInput(attrs={'placeholder': 'Ej: A'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Ej: 12'}),
        }

    # La manzana siempre se guarda en mayúsculas y sin espacios sobrantes
    def clean_manzana(self):
        return self.cleaned_data['manzana'].strip().upper()