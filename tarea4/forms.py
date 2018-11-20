from django import forms
from tarea4.models import *


class ResponderEval(forms.Form):
    fields = {}
    CHOICES = [('1', "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7")]
    for i in range(10):
        fields['pregunta' + str(i + 1)] = forms.ChoiceField(choices=CHOICES,
                                                                 widget=forms.RadioSelect(
                                                                     attrs={'class': "form-check-input"}))
