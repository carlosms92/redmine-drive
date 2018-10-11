from redminelib import Redmine
import time

redmine = Redmine('https://taquilla.antevenio.com/', username='', password='')

user = redmine.user.get('current',include=['memberships','groups'])
userId = user.id

date = time.strftime("%Y-%m-%d")

issues = redmine.issue.filter(
	assigned_to_id=userId,
	status_id="*",
	updated_on=date,
	sort='category:desc',
	include=['relations','journals']
)

for issue in issues:
	#ticket - proyecto - titulo - pais
	#print(list(issue))
	print(issue.id, " - " , issue.custom_fields[0].value, " - " ,issue.project.name, " - " , issue.subject)