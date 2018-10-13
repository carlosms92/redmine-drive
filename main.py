#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
from redmine_api import RedmineApi
#from drive_api.service import DriveService
from sheets_api.sheets_service import SheetsService

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="Redmine user")
parser.add_argument("-p", "--password", help="Redmine password")

args = parser.parse_args()

if args.username is None:
    sys.exit("Es necesario pasar el nombre de usuario de Redmine (option -u)")

if args.password is None:
    sys.exit("Es necesario pasar la contraseña de Redmine (option -p)")

#REDMINE
# redmine = RedmineApi(args.username, args.password)
# redmine.connect()
#
# userId = redmine.getCurrentUserId()
# dateYesterday = redmine.getYesterdayDate()
#
# issues = redmine.getUserIssuesByDate(userId,dateYesterday)
#
# for issue in issues:
#     print(issue.id, " - " , issue.custom_fields[0].value, " - " ,issue.project.name, " - " , issue.subject)

#DRIVE
#driveService = DriveService()
#driveService.getFile('1')

#SHEETS
sheetsService = SheetsService()
sheetsService.dailyUpdateSheet()
