#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import date, timedelta
import json

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


    def getSpreadsheet(self):
        ranges = []  # TODO: Update placeholder value.
        include_grid_data = False  # TODO: Update placeholder value.
        request = self.service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID, ranges=ranges, includeGridData=include_grid_data)
        response = request.execute()
        print(response)


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


    def dailyUpdateSheet(self, issues):
        yesterday = date.today() - timedelta(1)
        dateYesterday = yesterday.strftime("%d/%m/%Y")
        print(dateYesterday)
        range_ = 'Copia de 01/10 a 12/10!B13'
        value_input_option = 'RAW'
        insert_data_option = 'INSERT_ROWS'
        value_range_body = self.generateIssuesRequestBody(dateYesterday,issues)
        request = self.service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
        response = request.execute()
        return response


    def generateIssuesRequestBody(self, date, issues):
        values = []
        emptyRow = ["","","","","",""]
        dailyRow = [date,"Reunion","","TODOS","0,50","Daily"]
        values.append(emptyRow)
        values.append(dailyRow)

        for issue in issues:
            country = issue.custom_fields[0].value
            project = issue.project.name
            #title = issue.subject
            title = '#' + str(issue.id) + ' - ' + issue.subject
            row = [date,"Portales","",country,"",title]
            values.append(row)

        value_range_body = {"values": values}
        return value_range_body


    def updateFormatRange(self,range):
        top_header_format = [
            {'mergeCells': {
                'mergeType': 'MERGE_ROWS',
                'range': {
                    'endColumnIndex': 4,
                    'endRowIndex': 60,
                    'sheetId': '2027973397',
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
                  "sheetId": '2027973397',
                  "startRowIndex": 12,
                  "endRowIndex": 60,
                  "startColumnIndex": 5,
                  "endColumnIndex": 6
                },
                "cell": {
                  "userEnteredFormat": {
                    "numberFormat": {
                      "type": "NUMBER",
                      "pattern": "#0.00"
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
