# Propuesta para el sistema de coevaluaciones de ingenieria de software.
Por el grupo 4 del año 2018 semestre 2. Matias, Raul y Alex. (TODO: apellidos)

## Instalacion
Si todo salió bien, se deberia poder descargar el repositorio como un proyecto de django. Si no, se debe crear un proyecto primero y luego imoprtar los archivos (resolviendo conflictos de merge favoreciendo los archivos del repositorio).

## Archivos
En este repositorio se encuentran:
- la carpeta principal del proyecto de Django en PyCharm: coev. Con sus archivos.py necesarios.
- la carpeta del app  de coevlacion: Tarea 4. Con sus archivos.py necesarios.
- la carpeta templates que usa la app. Con sus html.
- el archivo manage.py
      
## Config del admin y base de datos.
Estos archivos no contienen ni la base de datos ni las migraciones, en cada proyecto se debe cargar la base de datos, generar la migracion inicial y cargar la migracion. Tambien deben setear el superuser.
- python manage.py migrate
- python manage.py makemigrations tarea4
- python manage.py migrate

## Uso de los ccs y js del mockup
Para hacer disponibles se debio guardar los archivos de css y js en la carpeta statis dentro de la carpeta de la app "tarea4", que esta dentro de la raiz del proyecto.
En los setings del proyecto se debe setear la ruta de static (ya esta en el repo).
Los archivos se cargan haciendo accesible la ruta con la variable static y se referencian con esta variable como raiz del elemento.
Esto tambien se usa para las imagenes (iconos) que estan en la carpeta static. (Nota estos archivos se cargan en demanda, no solo por
estar en la ruta)
Ejemplo.
- {% load static %}
- href="{% static 'tarea4/css/bootstrap.min.css' %}"
