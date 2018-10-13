from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
FILE_ID = '1tp8u2vCN94uCPra4rOarjCuhJcqqVi7PgWBq-IXpqRY'

class DriveService:

    def __init__(self):
        self.service = self.getAuthentication()

    def getAuthentication(self):
        #store = file.Storage('token.json')
        store = file.Storage('drive_api/token.json')
        creds = store.get()
        if not creds or creds.invalid:
            #flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            flow = client.flow_from_clientsecrets('drive_api/credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('drive', 'v3', http=creds.authorize(Http()))
        return service

    def getFilesList(self):
        results = self.service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))

    def getFile(self, fileId):
        fileId = FILE_ID
        file = self.service.files().get(fileId=fileId)
        print(file)

    def updateFile(self, fileId):
        fileId = FILE_ID
        print(fileId)
