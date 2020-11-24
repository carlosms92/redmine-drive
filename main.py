#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse, getpass
from datetime import datetime
from redmine_api import RedmineApi
from sheets_api.sheets_service import SheetsService

class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            values = getpass.getpass()

        setattr(namespace, self.dest, values)

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="Redmine user")
parser.add_argument("-p", "--password", action=Password, nargs="?", dest="password", help='Redmine password')

args = parser.parse_args()

if args.username is None:
    sys.exit("Es necesario pasar el nombre de usuario de Redmine (option -u)")

if args.password is None:
    sys.exit("Es necesario pasar la contraseña de Redmine (option -p)")


#REDMINE
redmine = RedmineApi(args.username, args.password)
redmine.connect()

userId = redmine.getCurrentUserId()
dateYesterday = redmine.getYesterdayDate()
dateYesterday = '2020-11-03'

issues = redmine.getUserIssuesByDate(userId,dateYesterday)

# for issue in issues:
#     print(list(issue))
#     print(issue.id, " - ", issue.custom_fields[0].value, " - ", issue.project.name, " - ", issue.subject)
# sys.exit(0)

#SHEETS
updateDate = datetime.strptime(dateYesterday,"%Y-%m-%d")

sheetsService = SheetsService()

#spreadsheet = sheetsService.getSpreadsheet()
#sheets = spreadsheet.get('sheets')

#for sheet in sheets:
#	print(sheet.get('properties'))

responseUpdateFields = sheetsService.dailyUpdateSheet(issues,updateDate)
updatedRange = responseUpdateFields['updates']['updatedRange']
print(updatedRange)
responseUpdateFormat = sheetsService.updateFormatRange(updatedRange)
print(responseUpdateFormat)
#responseUpdateFormatColumnToNumber = sheetsService.updateFormatColumnToNumber()
#print(responseUpdateFormatColumnToNumber)

#sheetsService.getSpreadsheet()
#sheetsService.getRow()
