from django.shortcuts import render
from tarea4.models import *

# Create your views here.
def landingPageEstudiantes(request):
    userID = 1; #placeholder para la id correcta.

    #nota dependiendo de como quede el modelo user, el filtro puede cambiar.
    cursosEstudiante = Curso.objects.filter(estudiante__user_id=userID)
    cursosDocente = Curso.objects.filter(docente__user_id=userID)


    coevaluacionesDocente = Coevaluacion.objects.filter(pregunta__preguntasdocentes__docente_id=userID)
    coevaluacionesEstudiante = Coevaluacion.objects.filter(pregunta__preguntasestudiantes__estudiante=userID).distinct()


    return render()


def perfilDueno(request):

    return render()

def fichaCursoEstudiante(request):

    return  render()

def fichaCursoDocente(request):

    return render()

def fichaCoevaluacionEstudiante(request):

    return render()