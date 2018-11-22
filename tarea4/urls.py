from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    # path('', views.index, name=''),
    # En este caso el string de path recibe un entero, y la variable tiene nombre humano. También se pueden usar regex.
    # El nombre de la url permite insertarla en la template usando {% url 'humano' %}
    #path('admin/', admin.site.urls),
    path('home/', views.landingPageEstudiante, name='landingPage'),
    path('repartidor/', views.repartidor, name='repartidor'),
    path('perfil/', views.perfilDueno, name='perfil'),
    path('fichaCursoDoc/<int:idCurso>', views.fichaCursoDocente, name='fichaCursoDocente'),
    path('fichaCursoEst/<int:idCurso>', views.fichaCursoEstudiante, name='fichaCursoEstudiante'),
    path('fichaCoev/<int:idCoev>', views.fichaCoevaluacionEstudiante, name='fichaCoevaluacion'),
    path('noentresaqui', views.fichaCoevEstHandler, name='responderCoev'),
    path('repartidorCurso/<int:idCurso>', views.fichaCurso, name='fichaCurso'),
    path('agregarCoev', views.agregarCoev, name='agregarCoev')

]