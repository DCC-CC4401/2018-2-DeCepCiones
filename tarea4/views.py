from django.shortcuts import render
from tarea4.models import *


# Create your views here.
def landingPageEstudiante(request):
    userID = 1;  # placeholder para la id correcta.

    # nota dependiendo de como quede el modelo user, el filtro puede cambiar.
    cursosEstudiante = Curso.objects.filter(estudiante__user_id=userID)
    cursosDocente = Curso.objects.filter(docente__user_id=userID)
    docentes = Docente.objects.filter(user_id=userID)
    coevaluaciones = Coevaluacion.objects.filter(curso__estudiante__user_id=userID)


    listaCurso =[]
    listaCoev = []
    for curso in cursosEstudiante:
        listaCurso.append({"cargo":"alumno", "nombre":curso.Nombre, "codigo":curso.Codigo+str(curso.Seccion), "semestre":str(curso.Ano)+" - "+str(curso.Semestre)})

    for curso in cursosDocente:
        listaCurso.append({"cargo": "auxiliar", "nombre":curso.Nombre, "codigo":curso.Codigo+str(curso.Seccion), "semestre":str(curso.Ano)+" - "+str(curso.Semestre)})

    for coev in coevaluaciones:
        listaCoev.append({})

    micoev = [{'estadoTr': "pendiente", 'fechaInicio': "asda", 'nombre': "ajaja", 'cursoNombre': "asdads", 'cursoCod':"poiopoi", 'cursoSemestre':"asd", 'fechaFin': "asda", 'responder':"Responder", 'estado':"Pendiente", 'cargo': "alumno"}]
    micurso = [{'cargo': "alumno", 'nombre':"asda", 'codigo':"67890", 'semestre':"67890p"}]


    return render(request, 'tarea4/landingPageEstudiante.html', {'listaCoev': micoev, 'listaCurso': micurso  })


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
