from django import forms
from tarea4.models import *


class ResponderEval(forms.Form):
    def init(self, *args, **kwargs):
        self.coevID = kwargs.pop('coevID')
        super(ResponderEval, self).init(*args, **kwargs)
        preguntas = Coevaluacion.objects.get(id=self.coevID).pregunta_set.order_by('indice')
        CHOICES = [('1', "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7")]
        for pregunta in preguntas:
            self.fields['pregunta' + str(pregunta.indice)] = forms.ChoiceField(choices=CHOICES,
                                                                               widget=forms.RadioSelect(
                                                                                   attrs={'class': "form-check-input"}))