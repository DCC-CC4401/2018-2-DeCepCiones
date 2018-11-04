from django.db import models

# Create your models here.

class Usuario(models.Model):
    ID = models.IntegerField(max_length=10, primary_key=True)
    rut = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50)
    email = models.EmailField()


class Grupo(models.Model):
    IDGrupo = models.IntegerField(max_length=10, primary_key=True)
    IDCurso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=50)


class Estudiante(models.Model):
    IDEstudiante = models.IntegerField(max_length=10, primary_key=True)
    IDUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


class GrupoEstudiante(models.Model):
    IDGrupo = models.ForeignKey(Grupo)
    IDEstudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    Periodo = models.DateField()


class Docente(models.Model):
    IDDocente = models.IntegerField(max_length=10, primary_key=True)
    IDUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=20)


class Coevaluacion(models.Model):
    IDCoevaluacion = models.IntegerField(max_length=10, primary_key=True)
    IDCurso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    Estado = models.CharField(max_lenght=20)
    Fecha_inicio = models.DateField()
    Fecha_termino = models.DateField()


class Preguntas(models.Model):
    IDPregunta = models.IntegerField(max_length=10)
    IDCoevalacion = models.ForeignKey(Coevaluacion, on_delete=models.CASCADE)
    Pregunta = models.CharField(max_length=250)         # estará bien con 250?


class PreguntasEstudiantes(models.Model):
    IDPregunta = models.ForeignKey(Preguntas)
    IDEstudiante = models.ForeignKey(Estudiante)
    Respuesta = models.CharField(max_length=250)


class Curso(models.Model):
    IDCurso = models.IntegerField(max_length=10, primary_key=True)
    Nombre = models.CharField(max_length=10)
    Codigo = models.CharField(max_length=10)
    Seccion = models.IntegerField(max_length=10)
    Ano = models.IntegerField(max_length=4)
    Semestre = models.CharField(max_length=10)


class EstudianteCurso(models.Model):
    IDDocente = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    IDCurso = models.ForeignKey(Curso, on_delete=models.CASCADE)


class DocenteCurso(models.Model):
    IDDocente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    IDCurso = models.ForeignKey(Curso, on_delete=models.CASCADE)

