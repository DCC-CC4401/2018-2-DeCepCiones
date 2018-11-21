from django import forms
from tarea4.models import *


class ResponderEval(forms.Form):
    fields = {}
    CHOICES = [('1', "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7")]
    pregunta1 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input"}))
    pregunta2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input"}))
    pregunta3 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input"}))
    pregunta4 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input"}))
    pregunta5 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input"}))
    pregunta6 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input"}))
    pregunta7 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input"}))
    pregunta8 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input"}))
    pregunta9 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input"}))
    pregunta10 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': "form-check-input"}))
