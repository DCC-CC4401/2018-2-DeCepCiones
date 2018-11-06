from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Curso(models.Model):
    Nombre = models.CharField(max_length=10)
    Codigo = models.CharField(max_length=10)
    Seccion = models.IntegerField()
    Ano = models.IntegerField()
    Semestre = models.CharField(max_length=10)


"""
la idea de usar user como abstracto es poder usar las funciones de validacion de django y poder setear nuestros atributos para user.
no se si funciona asi. revisar o preguntar.
"""
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # no se si esto funciona, Usuario es abstracto y user es el usuario de django.
    nombre = models.CharField(max_length=60)
    email = models.EmailField()

    class Meta:
        abstract = True


class Docente(Usuario):
    cargo = models.CharField(max_length=20)
    cursos = models.ManyToManyField(Curso)


class Estudiante(Usuario):
    cursos = models.ManyToManyField(Curso)


class Grupo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=50)
    Estado = models.CharField(max_length=50) # activo VS historico para efectos de historial.


class Coevaluacion(models.Model):
    estado = models.CharField(max_length=20)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)


class Pregunta(models.Model):
    pregunta = models.CharField(max_length=250)         # estará bien con 250?
    coevaluacion = models.ForeignKey(Coevaluacion, on_delete=models.CASCADE)


class PreguntasEstudiantes(models.Model):
    respuesta = models.CharField(max_length=250)
    estudianteRespondedor = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="evaluador")
    estudianteEvaluado = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="evaluado")
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)