from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime

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
    for curso in cursos.order_by('-Ano', '-Semestre'):
        listaCurso.append({"cargo": curso.usuariocurso_set.get(user=userID).cargo.lower(), "nombre": curso.Nombre,
                           "codigo": curso.Codigo + "-" + str(curso.Seccion),
                           "semestre": str(curso.Ano) + "-" + str(curso.Semestre),
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
        if contestada:
            estado = "contestada"
        elif coev.estado.lower() == "abierta":
            estado = "pendiente"
        else:
            estado = coev.estado.lower()

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

    for curso in listaCurso.order_by('-Ano', '-Semestre'):
        listaNotas = []
        for nota in notas.filter(coevaluacion__curso=curso.id):
            listaNotas.append({'nombre': nota.coevaluacion.nombre, 'publicada': str(nota.fecha_publicacion), 'nota': nota.nota})
        cursosEstudiante.append(
            {'cargo': UsuarioCurso.objects.get(curso=curso.id, user=userID).cargo.lower(), 'nombre': curso.Nombre, 'codigo': curso.Codigo + "-" + str(curso.Seccion),
             'semestre': str(curso.Ano) + "-" + str(curso.Semestre), 'notas': listaNotas, 'id': curso.id    })

    dueno = {'nombre': estudiante.first_name, 'nombreCompleto': estudiante.first_name + " " + estudiante.last_name,
             'email': estudiante.email, 'rut': estudiante.username}

    form = PasswordChangeForm(user=request.user)

    return render(request, 'perfilDueno.html', {'dueno': dueno, 'listaCurso': cursosEstudiante, 'contraseñaForm': form})


def fichaCursoEstudiante(request, idCurso):
    userID = request.user.id
    userNombre = request.user.first_name + " " + request.user.last_name
    curso = Curso.objects.get(id=idCurso)
    coevs = Coevaluacion.objects.filter(curso=idCurso, curso__usuariocurso__user=userID).order_by('-fecha_inicio')
    dataCurso = curso.Codigo + "-" + str(curso.Seccion) + " " + curso.Nombre + ", " + str(curso.Ano) + "-" + str(
        curso.Semestre)
    listaCoev = []

    for coev in coevs:
        grupo = Grupo.objects.get(curso=coev.curso, estudiante=userID).estudiante.all()
        contestada = True

        for integrante in grupo:
            if integrante.id != userID:
                if not Respuestas.objects.filter(coevaluacion=coev.id, estudianteEvaluado=integrante.id,
                                                 estudianteRespondedor=userID).exists():
                    contestada = False;
                    break
        estado = ""
        if contestada:
            estado = "contestada"
        elif coev.estado.lower() == "abierta":
            estado = "pendiente"
        else:
            estado = coev.estado.lower()

        listaCoev.append(
            {'fechaIni': coev.fecha_inicio, 'fechaTer': coev.fecha_termino, 'nombre': coev.nombre, 'estadoTr':
                estado, 'id': coev.id, 'estado': estado.capitalize()})

    return render(request, 'fichaCursoEstudiante.html', {'dataCurso': dataCurso, 'coevs': listaCoev, 'userNombre': userNombre})


def fichaCursoDocente(request, idCurso):
    userID = request.user.id
    userNombre = request.user.first_name + " " + request.user.last_name
    curso = Curso.objects.get(id=idCurso)
    coevs = Coevaluacion.objects.filter(curso=idCurso).order_by('-fecha_inicio')
    grupos = Grupo.objects.filter(curso=idCurso)
    estudiantes = User.objects.filter(usuariocurso__curso=idCurso, usuariocurso__cargo='estudiante')
    dataCurso = curso.Codigo + "-" + str(curso.Seccion) + " " + curso.Nombre + ", " + str(curso.Ano) + "-" + str(
        curso.Semestre)
    listaGrupos = []
    listaCoev = []
    listaEstudiantes = []
    nuevaCoev = agregarCoevForm()

    for estudiante in estudiantes:
        listaEstudiantes.append(estudiante.nombre)

    for grupo in grupos:
        listaTitulos = []
        listaAlumnos = []
        for alumno in grupo.estudiante.all():
            listaNotas = []
            listaTitulos = []
            for nota in NotaEstudiante.objects.filter(coevaluacion__curso=idCurso, estudiante=alumno.id).order_by(
                    'fecha_publicacion'):
                if nota != "":
                    listaNotas.append(nota.nota)
                    listaTitulos.append(nota.coevaluacion.nombre)
            listaAlumnos.append({'nombre': alumno.first_name + " " + alumno.last_name, 'notas': listaNotas})
        #for i in range(len(coevs)):
            #listaTitulos.append("nota " + str(i + 1))
        listaGrupos.append({'nombre': grupo.Nombre, 'titulos': listaTitulos, 'alumnos': listaAlumnos})

    for coev in coevs:
        listaCoev.append(
            {'fechaIni': coev.fecha_inicio, 'fechaTer': coev.fecha_termino, 'nombre': coev.nombre, 'estado':
                coev.estado.lower(), 'estadoPrint': coev.estado.lower().capitalize(), 'id': coev.id})

    return render(request, 'fichaCursoDocente.html', {'dataCurso': dataCurso, 'grupos': listaGrupos, 'coevs': listaCoev,
                                                      'estudiantes': listaEstudiantes, 'userNombre': userNombre,
                                                      'agregarCoev': nuevaCoev, 'idCurso': idCurso})


def fichaCoevaluacionEstudiante(request, idCoev):
    if (request.method=='POST'):
        a=1
    userID = request.user.id
    userNombre = request.user.first_name + " " + request.user.last_name
    coev = Coevaluacion.objects.get(id=idCoev)
    coevCurso = coev.curso
    est = User.objects.get(id=userID)
    grupo = est.grupo_set.get(curso=coevCurso.id)
    preguntas = Pregunta.objects.get(coevaluacion=idCoev)
    form = ResponderEval()
    listaIntegrantes = []
    coevContestada = True;
    for estudiante in grupo.estudiante.all():
        if estudiante.id != userID:
            contestada = Respuestas.objects.filter(estudianteEvaluado=estudiante.id, estudianteRespondedor=userID, coevaluacion=idCoev).exists()
            coevContestada = coevContestada and contestada
            listaIntegrantes.append( {'nombre': estudiante.first_name + " " + estudiante.last_name, 'id': estudiante.id,
                                      'contestada': contestada})
    estado = ""
    if coevContestada:
        estado = "contestada"
    elif coev.estado.lower() == "abierta":
        estado = "pendiente"
    else:
        estado = coev.estado.lower()

    infoCoev = {'nombre': coev.nombre,
                'datosCurso': coevCurso.Codigo + " " + coevCurso.Nombre + " " + str(coevCurso.Seccion) +
                              ", " + str(coevCurso.Ano) + "-" + str(coevCurso.Semestre),
                'fechaInicio': coev.fecha_inicio, 'fechaTermino': coev.fecha_termino,
                'estado': estado, 'estadoPrint': estado.capitalize()}
    listaPreguntas = {
        'pregunta1': preguntas.pregunta1,
        'pregunta2': preguntas.pregunta2,
        'pregunta3': preguntas.pregunta3,
        'pregunta4': preguntas.pregunta4,
        'pregunta5': preguntas.pregunta5,
        'pregunta6': preguntas.pregunta6,
        'pregunta7': preguntas.pregunta7,
        'pregunta8': preguntas.pregunta8,
        'pregunta9': preguntas.pregunta9,
        'pregunta10': preguntas.pregunta10,
    }


    return render(request, 'fichaCoevaluacionEstudiante.html', {'coev': infoCoev,'coevID':idCoev,'listaInt':listaIntegrantes,
                                                                'formulario':form, 'nombreGrupo':grupo.Nombre, 'userNombre': userNombre,
                                                                'listaPreguntas': listaPreguntas, 'userID': userID})


def fichaCoevEstHandler(request):
    if request.method == 'POST':
        form = ResponderEval(request.POST)
        if form.is_valid():
            idCoev = form.cleaned_data['idCoev']
            respuesta = Respuestas()
            respuesta.respuesta1 = form.cleaned_data['pregunta1']
            respuesta.respuesta2 = form.cleaned_data['pregunta2']
            respuesta.respuesta3 = form.cleaned_data['pregunta3']
            respuesta.respuesta4 = form.cleaned_data['pregunta4']
            respuesta.respuesta5 = form.cleaned_data['pregunta5']
            respuesta.respuesta6 = form.cleaned_data['pregunta6']
            respuesta.respuesta7 = form.cleaned_data['pregunta7']
            respuesta.respuesta8 = form.cleaned_data['pregunta8']
            respuesta.respuesta9 = form.cleaned_data['pregunta9']
            respuesta.respuesta10 = form.cleaned_data['pregunta10']
            respuesta.coevaluacion = Coevaluacion.objects.get(id=idCoev)
            respuesta.estudianteEvaluado = User.objects.get(id=form.cleaned_data['idEvaluado'])
            respuesta.estudianteRespondedor = User.objects.get(id=form.cleaned_data['idEvaluador'])
            respuesta.fechaRespuesta = datetime.now()
            respuesta.save()

            return redirect('fichaCoevaluacion', idCoev=idCoev)

    return redirect('landingPage')


def repartidor(request):
    userID = request.user.id
    cargos = UsuarioCurso.objects.filter(user=userID)

    alumno = True
    for cargo in cargos:
        if cargo.cargo != 'ALUMNO':
            alumno = False
            break

    if alumno:
        return redirect('landingPage')
    else:
        return redirect('perfil')

def fichaCurso(request, idCurso):
    userID = request.user.id
    cargos = UsuarioCurso.objects.filter(user=userID, curso=idCurso)

    if cargos.exists():
        alumno = True
        for cargo in cargos:
            if cargo.cargo != 'ALUMNO':
                alumno = False
                break

        if alumno:
            return redirect('fichaCursoEstudiante', idCurso=idCurso)
        else:
            return redirect('fichaCursoDocente', idCurso=idCurso)
    else:
        return redirect('repartidor')


def agregarCoev(request):
    if request.method == 'POST':
        form = agregarCoevForm(request.POST)
        if form.is_valid():
            idCurso = form.cleaned_data['idCurso']
            coev = Coevaluacion()
            coev.nombre = form.cleaned_data['nombre']
            coev.fecha_inicio = form.cleaned_data['fecha_inicio']
            coev.fecha_termino = form.cleaned_data['fecha_termino']
            coev.curso = Curso.objects.get(id=idCurso)
            coev.preguntas = Pregunta.objects.get(id=1)
            coev.save()

            return redirect('fichaCursoDocente', idCurso=idCurso)

    return redirect('fichaCursoDocente', idCurso=idCurso)