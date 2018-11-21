from django import forms
from tarea4.models import *


class ResponderEval(forms.Form):
    fields = {}
    CHOICES = [('1', "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7")]
    idCoev = forms.CharField(max_length=20, widget=forms.HiddenInput(attrs={'id': 'formCoevID'}), initial="-1")
    idEvaluado = forms.CharField    (max_length=20, widget=forms.HiddenInput(attrs={'id': 'formEvaluadoID'}), initial="-1")
    pregunta1 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
    pregunta2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
    pregunta3 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
    pregunta4 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
    pregunta5 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
    pregunta6 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
    pregunta7 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
    pregunta8 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
    pregunta9 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
    pregunta10 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input radio-inline"}))
