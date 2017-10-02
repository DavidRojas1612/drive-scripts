# Google Drive scripts

Proyecto que contiene varios scripts para manipular [Google Drive](drive.google.com) desde la consola utilizando *Python 3*.

Todos los scripts necesitan [credenciales OAuth 2.0](https://support.google.com/googleapi/answer/6158857?hl=en&authuser=1&ref_topic=7013279) para otorgar los permisos y el acceso a la API de Google Drive.

Se debe descargar como **client_secret.json** y guardar dentro de la carpeta de los scripts.

Las librerias necesarias se pueden instalar usando `pip3`:
* [Google API Client Library for Python](https://pypi.python.org/pypi/google-api-python-client/1.6.4)
 ```bashs
 $ pip3 install -U google-api-python-client
 ```
* [Magic](https://pypi.python.org/pypi/magic/0.1)
```bash
$ pip3 install -U python-magic
```

# Scripts:
+ ## drive_download.py
Descarga un archivo desde el *drive* del usuario y lo almacena en una nueva carpeta *downloads*.
+ ## drive_list.py
Simplemente lista los archivos que existen en el *drive* del usuario. Inicialmente usado para crear el script para descargar.
+ ## drive_upload.py
Sube un archivo a la carpeta raiz del *drive* del usuario. Indicando la ruta del archivo y el nombre que tendrá.

# Compatibilidad
* Python 3.4 y superior
