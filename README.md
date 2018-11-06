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
- python manage.py makemigrations polls
- python manage.py migrate
