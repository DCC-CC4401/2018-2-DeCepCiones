from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from tarea4.models import *
from tarea4.forms import *
from django.contrib.auth import *
from django.contrib import messages


# Create your views here.
def landingPageEstudiante(request):
    userID = request.user.id  # placeholder para la id correcta.
    cursos = Curso.objects.filter(usuariocurso__user=userID)
    coevals = Coevaluacion.objects.filter(curso__usuariocurso__user=userID).order_by('fecha_termino')
    listaCurso = []
    listaCoev = []
    for curso in cursos:
        listaCurso.append({"cargo": curso.usuariocurso_set.get(user=userID).cargo, "nombre": curso.Nombre,
                           "codigo": curso.Codigo + str(curso.Seccion),
                           "semestre": str(curso.Ano) + " - " + str(curso.Semestre),
                           "id": curso.id})

    for coev in coevals:
        # No estamos haciendo los estados como secundarios
        listaCoev.append({'estadoTr': coev.estado, 'fechaInicio': coev.fecha_inicio, 'nombre': coev.nombre,
                          'cursoNombre': coev.curso.Nombre, 'cursoCod': coev.curso.Codigo,
                          'cursoSemestre': str(coev.curso.Ano) + "-" + str(coev.curso.Semestre),
                          'fechaFin': coev.fecha_termino, 'estado': coev.estado, 'responder': 'responder',
                          'cargo': coev.curso.usuariocurso_set.get(user=userID).cargo, "id": coev.id})

    return render(request, 'landingPageEstudiante.html', {'listaCoev': listaCoev, 'listaCurso': listaCurso})


def perfilDueno(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'contraseña cambiada')

    userID = request.user.id    #placeholder
    listaCurso = Curso.objects.filter(estudiante__user_id__exact=userID)
    listaCoev = Coevaluacion.objects.filter(curso__estudiante__user_id=userID)
    estudiante = User.objects.get(user_id__exact=userID)
    cursosEstudiante = []


    for curso in listaCurso:
        cursosEstudiante.append(
            {'cargo': "alumno", 'nombre': curso.Nombre, 'codigo': curso.Codigo + "-" + str(curso.Seccion),
             'semestre': str(curso.Ano) + "-" + str(curso.Semestre)})
    dueno = {'nombre': estudiante.nombre, 'nombreCompleto': estudiante.nombre + " " + estudiante.apellido,
             'email': estudiante.email, 'rut': estudiante.rut}

    form = PasswordChangeForm(user=request.user)

    return render(request, 'perfilDueno.html', {'dueno': dueno, 'listaCurso': cursosEstudiante, 'contraseñaForm': form, 'listaCoev': listaCoev})


def fichaCursoEstudiante(request, idCurso):
    userID = request.user.id
    curso = Curso.objects.get(id=idCurso)
    coevs = Coevaluacion.objects.filter(curso=idCurso, curso__estudiante__user_id=userID)
    dataCurso = curso.Codigo + "-" + str(curso.Seccion) + " " + curso.Nombre + " " + str(curso.Ano) + ", " + str(
        curso.Semestre)
    listaCoev = []
    for coev in coevs:
        listaCoev.append(
            {'fechaIni': coev.fecha_inicio, 'fechaTer': coev.fecha_termino, 'nombre': coev.nombre, 'estado':
                coev.estado, 'id': coev.id})
    return render(request, 'fichaCursoEstudiante.html', {'dataCurso': dataCurso, 'coevs': listaCoev})


def fichaCursoDocente(request, idCurso):
    userID = request.user.id
    curso = Curso.objects.get(id=idCurso)
    coevs = Coevaluacion.objects.filter(curso=idCurso)
    grupos = Grupo.objects.filter(curso=idCurso)
    estudiantes = User.objects.filter(cursos=idCurso).distinct()
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
            for nota in NotaEstudiante.objects.filter(coevaluacion__curso=idCurso, estudiante=alumno.user.id).order_by(
                    'fecha_publicacion'):
                listaNotas.append(nota.nota)
            listaAlumnos.append({'nombre': alumno.nombre, 'notas': listaNotas})
        for i in range(len(coevs)):
            listaTitulos.append("nota " + str(i + 1))
        listaGrupos.append({'nombre': grupo.Nombre, 'titulos': listaTitulos, 'alumnos': listaAlumnos})

    for coev in coevs:
        listaCoev.append(
            {'fechaIni': coev.fecha_inicio, 'fechaTer': coev.fecha_termino, 'nombre': coev.nombre, 'estado':
                coev.estado, 'id': coev.id})

    return render(request, 'fichaCursoDocente.html', {'dataCurso': dataCurso, 'grupos': listaGrupos, 'coevs': listaCoev,
                                                      'estudiantes': listaEstudiantes})


def fichaCoevaluacionEstudiante(request, idCoev):
    if (request.method=='POST'):
        a=1
    userID = request.user.id
    coev = Coevaluacion.objects.get(id=idCoev)
    coevCurso = coev.curso
    est = User.objects.get(id=userID)
    grupo = est.grupo_set.get(curso=coevCurso.id)
    form = ResponderEval()
    infoCoev = {'nombre': coev.nombre,
                'datosCurso': coevCurso.Codigo + " " + coevCurso.Nombre + " " + str(coevCurso.Seccion) +
                              ", " + str(coevCurso.Ano) + "-" + str(coevCurso.Semestre),
                'fechaInicio': coev.fecha_inicio, 'fechaTermino': coev.fecha_termino,
                'estado': coev.estado}
    listaIntegrantes = {}
    for estudiante in grupo.estudiante.all():
        listaIntegrantes[estudiante.first_name + " " + estudiante.last_name]= estudiante.id
    return render(request, 'fichaCoevaluacionEstudiante.html', {'coev': infoCoev,'coevID':idCoev,'listaInt':listaIntegrantes,
                                                                'formulario':form, 'nombreGrupo':grupo.Nombre})

