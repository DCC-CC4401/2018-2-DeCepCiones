from django.shortcuts import render
from tarea4.models import *


# Create your views here.
def landingPageEstudiante(request):
    userID = request.user.id  # placeholder para la id correcta.

    # nota dependiendo de como quede el modelo user, el filtro puede cambiar.
    cursosEstudiante = Curso.objects.filter(estudiante__user_id=userID)
    cursosDocente = Curso.objects.filter(docente__user_id=userID)
    docentes = Docente.objects.filter(user_id=userID)
    coevaluaciones = Coevaluacion.objects.filter(curso__estudiante__user_id=userID)
    # coevaluaciones[0].curso.docente_set.filter(user_id__exact=userID)[0].cargo

    listaCurso = []
    listaCoev = []
    for curso in cursosEstudiante:
        listaCurso.append({"cargo":"alumno", "nombre":curso.Nombre, "codigo":curso.Codigo+str(curso.Seccion), "semestre":str(curso.Ano)+" - "+str(curso.Semestre), "id":curso.id})

    for curso in cursosDocente:
        listaCurso.append({"cargo": curso.docente_set.get(user_id__exact=userID).cargo, "nombre":curso.Nombre, "codigo":curso.Codigo+str(curso.Seccion), "semestre":str(curso.Ano)+" - "+str(curso.Semestre), "id":curso.id})

    for coev in coevaluaciones:
        # Revisar si hay cargo docente en el curso
        listaCoev.append({'estadoTr': coev.estado, 'fechaInicio': coev.fecha_inicio, 'nombre': coev.nombre, 'cursoNombre': coev.curso.Nombre, 'cursoCod': coev.curso.Codigo, 'cursoSemestre': str(coev.curso.Ano) + "-" + str(coev.curso.Semestre),
                          'fechaFin': coev.fecha_termino, 'estado': coev.estado, 'responder': 'responder', 'cargo': "alumno","id": coev.id})

    #micoev = [{'estadoTr': "pendiente", 'fechaInicio': "asda", 'nombre': "ajaja", 'cursoNombre': "asdads", 'cursoCod':"poiopoi", 'cursoSemestre':"asd", 'fechaFin': "asda", 'responder':"Responder", 'estado':"Pendiente", 'cargo': "alumno"}]
    #micurso = [{'cargo': "alumno", 'nombre':"asda", 'codigo':"67890", 'semestre':"67890p"}]


    return render(request, 'landingPageEstudiante.html', {'listaCoev': listaCoev, 'listaCurso': listaCurso  })


def perfilDueno(request):
    userID = 1 #placeholder
    listaCurso = Curso.objects.filter(estudiante__user_id__exact=userID)
    listaCoev = Coevaluacion.objects.filter(curso__estudiante__user_id=userID)
    estudiante = Estudiante.objects.get(user_id__exact=userID)
    cursosEstudiante = []

    for curso in listaCurso:
        cursosEstudiante.append({'cargo':"alumno", 'nombre':curso.Nombre, 'codigo': curso.Codigo + "-" + str(curso.Seccion),
                                 'semestre': str(curso.Ano) + "-" + str(curso.Semestre)})
    dueno = {'nombre': estudiante.nombre, 'nombreCompleto': estudiante.nombre + " " + estudiante.apellido,
             'email': estudiante.email, 'rut': estudiante.rut}

    return render(request, 'tarea4/perfilDueno.html', {'dueno': dueno, 'listaCurso': cursosEstudiante})


def fichaCursoEstudiante(request,idCurso):
    return render(request, 'tarea4/fichaCursoEstudiante.html')


def fichaCursoDocente(request,idCurso):
    return render(request, 'tarea4/fichaCursoDocente.html')


def fichaCoevaluacionEstudiante(request,idCoev):
    coev = Coevaluacion.objects.get(id=idCoev)
    coevCurso = coev.curso
    infoCoev = {'nombre': coev.nombre, 'datosCurso': coevCurso.Codigo + " " + coevCurso.Nombre + " " + str(coevCurso.Seccion) +
                ", " + str(coevCurso.Ano) + "-" + str(coevCurso.Semestre), 'fechaInicio': coev.fecha_inicio, 'fechaTermino': coev.fecha_termino,
                'estado': coev.estado}
    return render(request, 'tarea4/fichaCoevaluacionEstudiante.html', {'coev': infoCoev})
