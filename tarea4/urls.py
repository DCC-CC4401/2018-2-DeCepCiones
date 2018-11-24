from django.urls import path
from . import views


urlpatterns = [
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