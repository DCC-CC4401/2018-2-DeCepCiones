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

    return render(request, 'perfilDueno.html', {'dueno': dueno, 'listaCurso': cursosEstudiante})


def fichaCursoEstudiante(request, idCurso):
    userID = request.user.id
    curso = Curso.objects.get(id=idCurso)
    coevs = Coevaluacion.objects.filter(curso=idCurso, curso__estudiante__user_id=userID)
    dataCurso = curso.Codigo + "-" + str(curso.Seccion) + " " + curso.Nombre + " " + str(curso.Ano) + ", " + str(curso.Semestre)
    listaCoev = []
    for coev in coevs:
        listaCoev.append({'fechaIni': coev.fecha_inicio, 'fechaTer': coev.fecha_termino, 'nombre': coev.nombre, 'estado':
                          coev.estado, 'id': coev.id})
    return render(request, 'fichaCursoEstudiante.html', {'dataCurso': dataCurso, 'coevs': listaCoev})


def fichaCursoDocente(request,idCurso):
    userID = request.user.id
    curso = Curso.objects.get(id=idCurso)
    coevs = Coevaluacion.objects.filter(curso=idCurso)
    grupos = Grupo.objects.filter(curso=idCurso)
    estudiantes = Estudiante.objects.filter(cursos=idCurso).distinct()
    dataCurso = curso.Codigo + "-" + str(curso.Seccion) + " " + curso.Nombre + " " + str(curso.Ano) + ", " + str(
        curso.Semestre)
    listaGrupos = []
    listaCoev = []
    listaEstudiantes = []

    for estudiante in estudiantes:
        listaEstudiantes.append(estudiante.nombre)

    for grupo in grupos:
        listaTitulos = []
        listaAlumnos = []
        for alumno in curso.estudiante_set.all():
            listaNotas = []
            for nota in NotaEstudiante.objects.filter(coevaluacion__curso=idCurso, estudiante=alumno.user.id).order_by('fecha_publicacion'):
                listaNotas.append(nota.nota)
            listaAlumnos.append({'nombre': alumno.nombre, 'notas': listaNotas})
        for i in range(len(coevs)):
            listaTitulos.append("nota "+ str(i+1))
        listaGrupos.append({'nombre': grupo.Nombre, 'titulos': listaTitulos, 'alumnos': listaAlumnos})

    for coev in coevs:
        listaCoev.append({'fechaIni': coev.fecha_inicio, 'fechaTer': coev.fecha_termino, 'nombre': coev.nombre, 'estado':
                        coev.estado, 'id': coev.id})

    return render(request, 'fichaCursoDocente.html', {'dataCurso': dataCurso, 'grupos': listaGrupos, 'coevs': listaCoev,
                                                      'estudiantes': listaEstudiantes})


def fichaCoevaluacionEstudiante(request,idCoev):
    coev = Coevaluacion.objects.get(id=idCoev)
    coevCurso = coev.curso
    infoCoev = {'nombre': coev.nombre, 'datosCurso': coevCurso.Codigo + " " + coevCurso.Nombre + " " + str(coevCurso.Seccion) +
                ", " + str(coevCurso.Ano) + "-" + str(coevCurso.Semestre), 'fechaInicio': coev.fecha_inicio, 'fechaTermino': coev.fecha_termino,
                'estado': coev.estado}
    return render(request, 'fichaCoevaluacionEstudiante.html', {'coev': infoCoev})
