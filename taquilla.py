from redminelib import Redmine
from datetime import date, timedelta

redmine = Redmine('https://taquilla.antevenio.com/', username='', password='')

user = redmine.user.get('current',include=['memberships','groups'])
userId = user.id

yesterday = date.today() - timedelta(1)
dateYesterday = yesterday.strftime("%Y-%m-%d")

print(dateYesterday)

issues = redmine.issue.filter(
	assigned_to_id=userId,
	status_id="*",
	updated_on=dateYesterday,
	sort='category:desc',
	include=['relations','journals']
)

for issue in issues:
	#ticket - proyecto - titulo - pais
	#print(list(issue))
	print(issue.id, " - " , issue.custom_fields[0].value, " - " ,issue.project.name, " - " , issue.subject)

#con issue.time_entries se saca el tiempo dedicado (te lo da por dias)