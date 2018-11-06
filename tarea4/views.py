from django.shortcuts import render
from tarea4.models import *


# Create your views here.
def landingPageEstudiante(request):
    userID = 1;  # placeholder para la id correcta.

    # nota dependiendo de como quede el modelo user, el filtro puede cambiar.
    cursosEstudiante = Curso.objects.filter(estudiante__user_id=userID)
    cursosDocente = Curso.objects.filter(docente__user_id=userID)

    coevaluacionesDocente = Coevaluacion.objects.filter(pregunta__preguntasdocentes__docente_id=userID)
    coevaluacionesEstudiante = Coevaluacion.objects.filter(pregunta__preguntasestudiantes__estudiante=userID).distinct()

    return render(request, 'tarea4/landingPageEstudiante.html')


def perfilDueno(request):

    return render(request, 'tarea4/perfilDueno.html')


def fichaCursoEstudiante(request):
    return render(request, 'tarea4/fichaCursoEstudiante.html')


def fichaCursoDocente(request):
    return render(request, 'tarea4/fichaCursoDocente.html')


def fichaCoevaluacionEstudiante(request):
    cursoID = 1;
    coev = Coevaluacion.objects.filter(curso=cursoID)
    return render(request, 'tarea4/fichaCoevaluacionEstudiante.html', {'coev': coev})
