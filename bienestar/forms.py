from django import forms
from .models import Genero, Pregunta, Opcion, Audiencia
from django.db.models import Q

class InicioForm(forms.Form):
    nombre = forms.CharField(label="Tu nombre", max_length=80)
    genero = forms.ChoiceField(label="Género", choices=Genero.choices, widget=forms.RadioSelect)

class PreguntasForm(forms.Form):
    """
    Se construye dinámicamente según el género (muestra preguntas ALL + del género).
    """
    def __init__(self, genero, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qs = Pregunta.objects.filter(activo=True).filter(
            Q(audiencia=Audiencia.TODOS) | Q(audiencia=genero)
        )
        qs = qs.order_by('id')
        for p in qs:
            field_name = f"q_{p.id}"
            opciones = [(str(op.id), op.texto) for op in p.opciones.all().order_by('id')]
            self.fields[field_name] = forms.ChoiceField(
                label=p.texto, choices=opciones, widget=forms.RadioSelect, required=True
            )
