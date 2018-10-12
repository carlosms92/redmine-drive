#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
from redmine_api import RedmineApi
#from drive_api import auth

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="Redmine user")
parser.add_argument("-p", "--password", help="Redmine password")

args = parser.parse_args()

if args.username is None:
    sys.exit("Es necesario pasar el nombre de usuario de Redmine (option -u)")

if args.password is None:
    sys.exit("Es necesario pasar la contraseña de Redmine (option -p)")

redmine = RedmineApi(args.username, args.password)
redmine.connect()

userId = redmine.getCurrentUserId()
dateYesterday = redmine.getYesterdayDate()

issues = redmine.getUserIssuesByDate(userId,dateYesterday)

for issue in issues:
    print(issue.id, " - " , issue.custom_fields[0].value, " - " ,issue.project.name, " - " , issue.subject)

# serviceGoogleDrive = getAuthentication()
#
# results = serviceGoogleDrive.files().list(
#     pageSize=10, fields="nextPageToken, files(id, name)").execute()
# items = results.get('files', [])
#
# if not items:
#     print('No files found.')
# else:
#     print('Files:')
#     for item in items:
#         print(u'{0} ({1})'.format(item['name'], item['id']))
