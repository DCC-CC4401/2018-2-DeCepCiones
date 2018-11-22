from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from tarea4.models import *
from tarea4.forms import *
from django.contrib.auth import *
from django.contrib import messages


# Create your views here.
def landingPageEstudiante(request):
    userID = request.user.id  # placeholder para la id correcta.
    userNombre = request.user.first_name + " " + request.user.last_name
    cursos = Curso.objects.filter(usuariocurso__user=userID)
    coevals = Coevaluacion.objects.filter(curso__usuariocurso__user=userID).order_by('-fecha_inicio')
    listaCurso = []
    listaCoev = []
    cont = 0;
    for curso in cursos:
        listaCurso.append({"cargo": curso.usuariocurso_set.get(user=userID).cargo.lower(), "nombre": curso.Nombre,
                           "codigo": curso.Codigo + str(curso.Seccion),
                           "semestre": str(curso.Ano) + " - " + str(curso.Semestre),
                           "id": curso.id})

    for coev in coevals:
        if cont >= 10:
            break
        # No estamos haciendo los estados como secundarios
        grupo = Grupo.objects.get(curso=coev.curso, estudiante=userID).estudiante.all()
        contestada = True

        for integrante in grupo:
            if integrante.id != userID:
                if not Respuestas.objects.filter(coevaluacion=coev.id, estudianteEvaluado=integrante.id, estudianteRespondedor=userID).exists():
                    contestada = False;
                    break
        estado = ""
        print(coev.estado)
        if contestada:
            estado = "contestada"
        elif coev.estado.lower() == "abierta"   :
            estado = "pendiente"
        else:
            estado = "cerrada"

        listaCoev.append({'estadoTr': estado, 'fechaInicio': coev.fecha_inicio, 'nombre': coev.nombre,
                          'cursoNombre': coev.curso.Nombre, 'cursoCod': coev.curso.Codigo,
                          'cursoSemestre': str(coev.curso.Ano) + "-" + str(coev.curso.Semestre),
                          'fechaFin': coev.fecha_termino, 'estado': estado.capitalize(),
                          'cargo': coev.curso.usuariocurso_set.get(user=userID).cargo.lower(), "id": coev.id})
        cont += 1

    return render(request, 'landingPageEstudiante.html', {'listaCoev': listaCoev, 'listaCurso': listaCurso, 'userNombre': userNombre})


def perfilDueno(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'contraseña cambiada')

    userID = request.user.id    #placeholder
    listaCurso = Curso.objects.filter(usuariocurso__user=userID)
    notas = NotaEstudiante.objects.filter(estudiante=userID)
    estudiante = User.objects.get(id=userID)
    cursosEstudiante = []

    for curso in listaCurso:
        listaNotas = []
        for nota in notas.filter(coevaluacion__curso=curso.id):
            listaNotas.append({'nombre': nota.coevaluacion.nombre, 'publicada': str(nota.fecha_publicacion), 'nota': nota.nota})
        cursosEstudiante.append(
            {'cargo': UsuarioCurso.objects.get(cursos=curso.id, user=userID).cargo.lower(), 'nombre': curso.Nombre, 'codigo': curso.Codigo + "-" + str(curso.Seccion),
             'semestre': str(curso.Ano) + "-" + str(curso.Semestre), 'notas': listaNotas})

    dueno = {'nombre': estudiante.first_name, 'nombreCompleto': estudiante.first_name + " " + estudiante.last_name,
             'email': estudiante.email, 'rut': estudiante.username}

    form = PasswordChangeForm(user=request.user)

    return render(request, 'perfilDueno.html', {'dueno': dueno, 'listaCurso': cursosEstudiante, 'contraseñaForm': form})


def fichaCursoEstudiante(request, idCurso):
    userID = request.user.id
    userNombre = request.user.first_name + " " + request.user.last_name
    curso = Curso.objects.get(id=idCurso)
    coevs = Coevaluacion.objects.filter(curso=idCurso, curso__usuariocurso__user=userID)
    dataCurso = curso.Codigo + "-" + str(curso.Seccion) + " " + curso.Nombre + " " + str(curso.Ano) + ", " + str(
        curso.Semestre)
    listaCoev = []
    for coev in coevs:
        listaCoev.append(
            {'fechaIni': coev.fecha_inicio, 'fechaTer': coev.fecha_termino, 'nombre': coev.nombre, 'estado':
                coev.estado, 'id': coev.id})
    return render(request, 'fichaCursoEstudiante.html', {'dataCurso': dataCurso, 'coevs': listaCoev, 'userNombre': userNombre})


def fichaCursoDocente(request, idCurso):
    userID = request.user.id
    userNombre = request.user.first_name + " " + request.user.last_name
    curso = Curso.objects.get(id=idCurso)
    coevs = Coevaluacion.objects.filter(curso=idCurso)
    grupos = Grupo.objects.filter(curso=idCurso)
    estudiantes = User.objects.filter(usuariocurso__cursos=idCurso, usuariocurso__cargo='estudiante')
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
        for alumno in grupo.estudiante.all():
            listaNotas = []
            for nota in NotaEstudiante.objects.filter(coevaluacion__curso=idCurso, estudiante=alumno.id).order_by(
                    'fecha_publicacion'):
                listaNotas.append(nota.nota)
            listaAlumnos.append({'nombre': alumno.first_name + " " + alumno.last_name, 'notas': listaNotas})
        for i in range(len(coevs)):
            listaTitulos.append("nota " + str(i + 1))
        listaGrupos.append({'nombre': grupo.Nombre, 'titulos': listaTitulos, 'alumnos': listaAlumnos})

    for coev in coevs:
        listaCoev.append(
            {'fechaIni': coev.fecha_inicio, 'fechaTer': coev.fecha_termino, 'nombre': coev.nombre, 'estado':
                coev.estado, 'id': coev.id})

    return render(request, 'fichaCursoDocente.html', {'dataCurso': dataCurso, 'grupos': listaGrupos, 'coevs': listaCoev,
                                                      'estudiantes': listaEstudiantes, 'userNombre': userNombre})


def fichaCoevaluacionEstudiante(request, idCoev):
    if (request.method=='POST'):
        a=1
    userID = request.user.id
    userNombre = request.user.first_name + " " + request.user.last_name
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
    listaIntegrantes = []
    for estudiante in grupo.estudiante.all():
        if(estudiante.id != userID):
            listaIntegrantes.append( {'nombre': estudiante.first_name + " " + estudiante.last_name, 'id': estudiante.id})
    return render(request, 'fichaCoevaluacionEstudiante.html', {'coev': infoCoev,'coevID':idCoev,'listaInt':listaIntegrantes,
                                                                'formulario':form, 'nombreGrupo':grupo.Nombre, 'userNombre': userNombre})

