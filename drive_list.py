import sys
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

#Recibe el ID y el SECRET como parametros
client_id = sys.argv[1]
client_secret = sys.argv[2]

SCOPES = 'https://www.googleapis.com/auth/drive.readonly.metadata'

def listFiles(drive):
    """Recibe el servicio y lista lor archivos"""
    files = drive.files().list().execute().get('files', [])
    for f in files:
        print(f['name'], f['mimeType'],f['id'])

def main():
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.OAuth2WebServerFlow(client_id, client_secret, SCOPES)
        creds = tools.run_flow(flow, store, tools.argparser.parse_args())
    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))
    listFiles(DRIVE)


if __name__ == "__main__":
    main()
