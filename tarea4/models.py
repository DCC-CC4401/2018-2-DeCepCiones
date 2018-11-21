from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Curso(models.Model):
    class Meta:
        unique_together = (('Codigo', 'Seccion', 'Ano', 'Semestre'),)

    Nombre = models.CharField(max_length=10)
    Codigo = models.CharField(max_length=10)
    Seccion = models.IntegerField()
    Ano = models.IntegerField()
    Semestre = models.CharField(max_length=10)


"""
la idea de usar user como abstracto es poder usar las funciones de validacion de django y poder setear nuestros atributos para user.
no se si funciona asi. revisar o preguntar.
"""


class UsuarioCurso(models.Model):
    listaCargos = (
        ('ALUMNO', 'alumno'), ('AUXILIAR', 'auxiliar'), ('AYUDANTE', 'ayudante'), ('PROFESOR', 'profesor'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=20, choices=listaCargos, default='alumno')
    cursos = models.ForeignKey(Curso, on_delete=models.CASCADE)


class Grupo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    estudiante = models.ManyToManyField(User)
    Nombre = models.CharField(max_length=50)
    Estado = models.CharField(max_length=50)  # activo VS historico para efectos de historial.


class Pregunta(models.Model):
    pregunta1 = models.CharField(max_length=250)
    pregunta2 = models.CharField(max_length=250)
    pregunta3 = models.CharField(max_length=250)
    pregunta4 = models.CharField(max_length=250)
    pregunta5 = models.CharField(max_length=250)
    pregunta6 = models.CharField(max_length=250)
    pregunta7 = models.CharField(max_length=250)
    pregunta8 = models.CharField(max_length=250)
    pregunta9 = models.CharField(max_length=250)
    pregunta10 = models.CharField(max_length=250)


class Coevaluacion(models.Model):
    nombre = models.CharField(max_length=30)
    listaEstados = (('ABIERTO', 'abierto'), ('CERRADO', 'cerrado'))
    estado = models.CharField(max_length=20, choices=listaEstados, default='abierto')
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    preguntas = models.ForeignKey(Pregunta, on_delete=models.SET_NULL, null=True)


class Respuestas(models.Model):
    coevaluacion = models.ForeignKey(Coevaluacion, on_delete=models.CASCADE)
    fechaRespuesta = models.DateField()
    respuesta1 = models.CharField(max_length=10)
    respuesta2 = models.CharField(max_length=10)
    respuesta3 = models.CharField(max_length=10)
    respuesta4 = models.CharField(max_length=10)
    respuesta5 = models.CharField(max_length=10)
    respuesta6 = models.CharField(max_length=10)
    respuesta7 = models.CharField(max_length=10)
    respuesta8 = models.CharField(max_length=10)
    respuesta9 = models.CharField(max_length=250)
    respuesta10 = models.CharField(max_length=250)
    estudianteRespondedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="evaluador")
    estudianteEvaluado = models.ForeignKey(User, on_delete=models.CASCADE, related_name="evaluado")


class HistorialGrupos(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()


class NotaEstudiante(models.Model):
    coevaluacion = models.ForeignKey(Coevaluacion, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.CharField(max_length=10)
    fecha_publicacion = models.DateField()
