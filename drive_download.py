from __future__ import print_function

from apiclient import discovery
from apiclient.http import MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools
from os import path, makedirs
from io import FileIO

# Scopes para autorización
SCOPES = ('https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file')

def servicio():
    """Construye el servicio de Google Drive.

    El archivo client_secret del usuario debe estar en la misma carpeta del script.

    Retorna el servicio."""
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        try:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        except:
            print('No se encontró el archivo client_secret.json')
            raise SystemExit
    drive = discovery.build('drive', 'v3', http=creds.authorize(Http()))
    return drive

def buscarArchivo(drive, nombre):
    """Hace la búsqueda del archivo a descargar y lo(s) lista.

    Argumentos:
    drive -- servicio para realizar la exportación
    nombre -- es el nombre del archivo que se va a buscar. Se listan los que coinciden
              con la búsqueda. Si viene vacío,  se listan todos los archivos del drive.

    Retorna el array de archivos con los atributos.
    """
    query = 'name contains "'+nombre+'" and (mimeType contains "image/" or mimeType contains "video/" or mimeType contains "application/" or mimeType contains "text/") and mimeType != "application/vnd.google-apps.folder"'
    #Petición y respuesta.
    file = drive.files().list(q=query, fields='files(id,mimeType,name, size)').execute().get('files', {})
    #Lista todos los archivos que coinciden con la busqueda.
    for f in file:
        print('ID: {id} \t {name} '.format(**f))
    return file


def download(drive, file, file_id):
    """Función que realiza la descarga del archivo.

    Argumentos:
    drive -- servicio para realizar la exportación
    file: -- el array del o los archivos
    file_id: -- necesario para buscar el archivo en el array y obtener
                sus atributos para exportar correctamente.
    """
    #Mimetypes de google
    googlemime = ['application/vnd.google-apps.document', 'application/vnd.google-apps.spreadsheet', 'application/vnd.google-apps.presentation']
    #Mimetypes de microsoft para expordar los documentos con mayor compatibilidad(la otra opcion es todos a pdf)
    msmimes = ['application/vnd.openxmlformats-officedocument.wordprocessingml.document',               'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.openxmlformats-officedocument.presentationml.presentation']
    mimeType = None
    nombre = None
    #Encuentra el nombre,el mimetype y peso del archivo a descargar(si es google-doc no tiene atributo peso)
    for f in file:
        if(f['id'] == file_id):
            nombre = f['name']
            mimeType = f['mimeType']
            try:
                size = float(f['size'])/1024
            except:
                continue #Continua la siguiente iteración si no tiene peso
    #Validación de los mimetypes en caso de que sean de google exportar a ms
    if(mimeType == googlemime[0]):
        request = drive.files().export_media(fileId=file_id, mimeType=msmimes[0])
    elif(mimeType == googlemime[1]):
        request = drive.files().export_media(fileId=file_id, mimeType=msmimes[1])
    elif(mimeType == googlemime[2]):
        request = drive.files().export_media(fileId=file_id, mimeType=msmimes[2])
    else:
        #Si no es google-doc se utiliza otro metodo (get_media) para exportar el archivo.
        request = drive.files().get_media(fileId=file_id)
    #Si no se ingresa el id, la variable nombre queda en None por lo tanto no se encuentra el id del archivo y no se puede descargar
    try:
        if ((not path.exists('downloads')) and nombre != None):
            makedirs('downloads')
        fh = FileIO('downloads/'+nombre, mode='wb')
    except:
        return print('¡¡¡No se encontró el valor!!!')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Downloading {:.1f}%".format(status.progress() * 100))
    #Los google-docs no aparecen con peso en la consulta a la api
    try:
        print('Descarga Completa! {} {:.2f}Kb'.format(nombre, size))
    except:
        print('Descarga Completa! {}'.format(nombre))

def main():
    """Realiza los llamados a las funciones y los valores ingresados por el usuario."""
    drive = servicio()
    nombre = input('Archivo a buscar [todos]: ')
    file = buscarArchivo(drive,nombre)
    id = input('Ingrese el ID a descargar: ')
    download(drive, file, id)

if __name__ == '__main__':
    main()
