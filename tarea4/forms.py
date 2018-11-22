from django import forms
from tarea4.models import *


class ResponderEval(forms.Form):
    CHOICES = [('1', "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7")]
    idCoev = forms.CharField(max_length=20, widget=forms.HiddenInput(attrs={'id': 'formCoevID'}), initial="-1")
    idEvaluador = forms.CharField(max_length=20, widget=forms.HiddenInput(attrs={'id': 'formEvaluadorID'}), initial="-1")
    idEvaluado = forms.CharField(max_length=20, widget=forms.HiddenInput(attrs={'id': 'formEvaluadoID'}), initial="-1")
    pregunta1 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
    pregunta2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
    pregunta3 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
    pregunta4 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
    pregunta5 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
    pregunta6 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
    pregunta7 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
    pregunta8 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
    pregunta9 = forms.CharField(max_length=250, widget=forms.Textarea)
    pregunta10 = forms.CharField(max_length=250, widget=forms.Textarea)


class agregarCoevForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    fecha_inicio = forms.DateField()
    fecha_termino = forms.DateField()
    idCurso = forms.CharField(max_length=20, widget=forms.HiddenInput(attrs={'id': 'formCursoID'}), initial="-1")