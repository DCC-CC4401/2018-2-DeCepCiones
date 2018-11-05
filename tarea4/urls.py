from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name=''),
    # En este caso el string de path recibe un entero, y la variable tiene nombre humano. También se pueden usar regex.
    # El nombre de la url permite insertarla en la template usando {% url 'humano' %}
    path('<int:id>', views.landingPageEstudiante, name='userid')
]