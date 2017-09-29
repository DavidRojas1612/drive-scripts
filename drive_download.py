from __future__ import print_function

from apiclient import discovery
from apiclient.http import MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools
import io

SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

files = DRIVE.files().list().execute().get('files', [])

file_id = '0B1z_D0coVaFnUkJ4TTI3WUlBT0U'
nombre = 'algo'
for f in files:
    print(f)
    if(file_id==f['id']):
        nombre = f['name']
        mime = f['mimeType']
print(nombre)
print(mime)

request = DRIVE.files().get_media(fileId=file_id)
fh = io.FileIO(nombre, mode='wb')
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print ("Download {:d}%".format(status.progress() * 100))