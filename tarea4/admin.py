from django.contrib import admin
from tarea4.models import *

# Register your models here.
admin.site.register(Curso)
admin.site.register(Docente)
admin.site.register(Estudiante)
admin.site.register(Grupo)
admin.site.register(Coevaluacion)
admin.site.register(Pregunta)
admin.site.register(PreguntasEstudiantes)
admin.site.register(PreguntasDocentes)