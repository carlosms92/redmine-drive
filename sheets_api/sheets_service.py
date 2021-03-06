#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle, json, sys, os

# If modifying these scopes, delete the file token.pickle
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

#2020
SPREADSHEET_ID = '1PqPNGfwI5sCOO4_63xTreFrZupuLXXdO8kv_8nCgpvs'
#24/06 a 05/07
#SHEET_ID = '1324422097'
SHEET_ID = '489188953'
#24/06 a 05/07
#DAILY_UPDATE_RANGE = '24/06 a 05/07!B13'
DAILY_UPDATE_RANGE = 'test!B13'

class SheetsService:

    def __init__(self):
        self.folder = os.path.dirname(os.path.abspath(__file__))
        self.service = self.getAuthentication()

    def getAuthentication(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'sheets_api/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        service = build('sheets', 'v4', credentials=creds)
        return service

    def getSpreadsheet(self):
        ranges = []  # TODO: Update placeholder value.
        include_grid_data = False  # TODO: Update placeholder value.
        request = self.service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID, ranges=ranges, includeGridData=include_grid_data)
        response = request.execute()
        return response


    def getSheet(self):
        range = 'Hoja 1!A1:C3'
        result = self.service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,range=range).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            for row in values:
                print(row)


    def getRow(self):
        result = self.service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range='Copia de 01/10 a 12/10!B16:G16').execute()
        row = result.get('values')
        json_row = json.dumps(row)
        print(json_row)
        #numRows = result.get('values') if result.get('values')is not None else 0
        #print('{0} rows retrieved.'.format(numRows));


    def dailyUpdateSheet(self, issues, updateDate):
        updateDate = updateDate.strftime("%d/%m/%Y")
        range_ = DAILY_UPDATE_RANGE
        value_input_option = 'USER_ENTERED'
        insert_data_option = 'INSERT_ROWS'
        value_range_body = self.generateIssuesRequestBody(updateDate,issues)
        request = self.service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
        response = request.execute()
        return response


    def generateIssuesRequestBody(self, date, issues):
        values = []
        #emptyRow = ["","","","","",""]
        dailyRow = [date,"Reunion","","TODOS","0.50","Daily"]
        #values.append(emptyRow)
        values.append(dailyRow)

        for issue in issues:
            try:
                country = self.mappingCountryValues(issue.custom_fields[0].value)
            except:
                country = 'TODOS'

            project = issue.project.name
            #title = issue.subject
            title = '#' + str(issue.id) + ' - ' + issue.subject
            row = [date,"Portales","",country,"",title]
            values.append(row)

        value_range_body = {"values": values}
        return value_range_body

    def mappingCountryValues(self, value):

        redmineCountryValues = ['ALL','ES','MX','IT','FR','USA']

        if value == 'ALL' or value not in redmineCountryValues:
            value = 'TODOS'

        return value

    def updateFormatRange(self,range):
        top_header_format = [
            {'mergeCells': {
                'mergeType': 'MERGE_ROWS',
                'range': {
                    'endColumnIndex': 4,
                    'endRowIndex': 60,
                    'sheetId': SHEET_ID,
                    'startColumnIndex': 2,
                    'startRowIndex': 12
                }
            }}
        ]

        batch_update_values_request_body = {
            'requests': top_header_format
        }
        request = self.service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=batch_update_values_request_body)
        response = request.execute()
        return response

    def updateFormatColumnToNumber(self):
        top_header_format = [
            {"repeatCell": {
                "range": {
                  "sheetId": SHEET_ID,
                  "startRowIndex": 12,
                  "endRowIndex": 60,
                  "startColumnIndex": 5,
                  "endColumnIndex": 6
                },
                "cell": {
                  "userEnteredValue": {
                    "stringValue": "1000"
                  },
                  "formattedValue": "1000",
                  "userEnteredFormat": {
                    "numberFormat": {
                      "type": "NUMBER",
                      "pattern": "#.##"
                    }
                  }
                },
                "fields": "userEnteredFormat.numberFormat"
              }}
        ]

        batch_update_values_request_body = {
            'requests': top_header_format
        }
        request = self.service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=batch_update_values_request_body)
        response = request.execute()
        return response


    #EXAMPLE VALUE RANGE BODY
    #value_range_body = {
        #    "values": [
        #        ["","","","",""],
        #        [
        #          dateYesterday,
        #          "Reunion",
        #          "",
        #          "TODOS",
        #          "0.50",
        #          "Daily"
        #        ],
        #        [
        #          dateYesterday,
        #          "Portales",
        #          "",
        #          "IT",
        #          "5.00",
        #          "Soporte #64236 - Club per Voi - Integration"
        #        ],
        #        [
        #          dateYesterday,
        #          "Reunion",
        #          "",
        #          "IT",
        #          "2.25",
        #          "Tareas #64090 - Añadir en la master DB la fecha de modificación de cada campo legal"
        #        ]
        #     ]
        #}
