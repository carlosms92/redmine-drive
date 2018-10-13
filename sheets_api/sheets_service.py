#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import date, timedelta

# If modifying these scopes, delete the file token.json.
#SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
SPREADSHEET_ID = '1tp8u2vCN94uCPra4rOarjCuhJcqqVi7PgWBq-IXpqRY'

class SheetsService:

    def __init__(self):
        self.service = self.getAuthentication()

    def getAuthentication(self):
        #store = file.Storage('token.json')
        store = file.Storage('sheets_api/token.json')
        creds = store.get()
        if not creds or creds.invalid:
            #flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            flow = client.flow_from_clientsecrets('sheets_api/credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('sheets', 'v4', http=creds.authorize(Http()))
        return service

    def getSheet(self):
        range = 'Hoja 1!A1:C3'
        result = self.service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                    range=range).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            for row in values:
                print(row)
                # Print columns A and E, which correspond to indices 0 and 4.
                #print('%s, %s' % (row[0], row[1]))

    def dailyUpdateSheet(self):
        yesterday = date.today() - timedelta(1)
        dateYesterday = yesterday.strftime("%d/%m/%Y")
        # The A1 notation of a range to search for a logical table of data.
        # Values will be appended after the last row of the table.
        range_ = 'Copia de 01/10 a 12/10!B13'

        # How the input data should be interpreted.
        value_input_option = 'RAW'

        # How the input data should be inserted.
        insert_data_option = 'INSERT_ROWS'

        value_range_body = {
            "values": [
                [
                  dateYesterday,
                  "Reunion",
                  "TODOS",
                  "0,5",
                  "Daily"
                ],
                [
                  dateYesterday,
                  "Portales",
                  "IT",
                  "5",
                  "Soporte #64236 - Club per Voi - Integration"
                ],
                [
                  dateYesterday,
                  "Reunion",
                  "IT",
                  "2,25",
                  "Tareas #64090 - Añadir en la master DB la fecha de modificación de cada campo legal"
                ]
             ]
        }

        request = self.service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
        response = request.execute()
        print(response)
