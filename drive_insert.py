from __future__ import print_function

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload
import magic
from sys import argv

def autorizacion():
    '''Funcion que autoriza los permisos en la cuenta de google '''
    SCOPES = 'https://www.googleapis.com/auth/drive.file'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
      flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
      creds = tools.run_flow(flow, store)
    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

    return DRIVE


def push(ruta,nombre,DRIVE,tipoArchivo):
	'''Funcion que sube el archivo deseado, pidiendo la ruta del archivo , el nombre, la autorizacion y  tipo de archivo'''
	archivo = {'name':nombre}
	media =  MediaFileUpload(ruta,mimetype=tipoArchivo,resumable=True)
	files = DRIVE.files().create(body=archivo,media_body=media,fields='id')
	respuesta = None
	while respuesta is None:
		status, respuesta = files.next_chunk()
		if status:
			print ('Subiendo {:.1f} %'.format(status.progress()*100))
	print ('Done!, el id del archivo subido es: {0}'.format(respuesta.get('id')))

def tipoArchivo(ruta):
	'''Funcion recibe la ruta del archivo y apartir de ella  extrae el  tipo del archivo que será subido'''
	mime = magic.Magic(mime=True)
	type = mime.from_file(ruta)
	return type

#ruta = str(argv[1])
nombre = input('escriba nombre del archivo: ')
ruta = input('esriba ruta del archivo: ')
ruta = ruta.replace('\'','')
tipo = tipoArchivo(ruta)



push(ruta,nombre,autorizacion(),tipo)
