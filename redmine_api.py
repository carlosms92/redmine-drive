from redminelib import Redmine
from datetime import date, timedelta

class RedmineApi:

	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.url = 'https://taquilla.antevenio.com/'
		self.connection = None

	def connect(self):
		self.connection = Redmine(self.url, username=self.username, password=self.password)

	def getYesterdayDate(self):
		yesterday = date.today() - timedelta(1)
		dateYesterday = yesterday.strftime("%Y-%m-%d")
		return dateYesterday

	def getCurrentUserId(self):
		user = self.connection.user.get('current',include=['memberships','groups'])
		userId = user.id
		return userId

	def getUserIssuesByDate(self, userId, date):
		issues = self.connection.issue.filter(
			assigned_to_id=userId,
			status_id="*",
			updated_on=date,
			sort='category:desc',
			include=['relations','journals']
		)
		return issues

	#con estos argumentos tenemos:

	# [(u'status', {u'id': 2, u'name': u'Asignada'}),
	# (u'project', {u'id': 117, u'name': u'SaludEnvidiable'}),
	# (u'attachments', None),
	# (u'time_entries', None),
	# (u'estimated_hours', 6.0),
	# (u'journals', None),
	# (u'children', None),
	# (u'custom_fields', [{u'id': 5, u'value': u'ES', u'name': u'Country'}]),
	# (u'description', u'Os paso el html.\r\n\r\nMuchas gracias'), (u'changesets', None),
	# (u'watchers', None), (u'author', {u'id': 159, u'name': u'David Clemente'}),
	# (u'created_on', u'2018-09-20T11:26:10Z'), (u'relations', []),
	# (u'id', 64291),
	# (u'priority', {u'id': 5, u'name': u'Alta'}),
	# (u'tracker', {u'id': 2, u'name': u'Tareas'}),
	# (u'fixed_version', {u'id': 72, u'name': u'Sprint 2018-19'}),
	# (u'assigned_to', {u'id': 746, u'name': u'Carlos Mart\xednez'}),
	# (u'updated_on', u'2018-10-10T07:33:01Z'),
	# (u'subject', u'Cambiar Welcome de usuario duplicado en Salud Envidiable'),
	# (u'start_date', u'2018-09-20'),
	# (u'done_ratio', 0)]

	#Si no pasamos include=['relations','journals'] tenemos:

	# [(u'status', {u'id': 2, u'name': u'Asignada'}),
	# (u'project', {u'id': 117, u'name': u'SaludEnvidiable'}),
	# (u'attachments', None), (u'time_entries', None),
	# (u'estimated_hours', 6.0),
	# (u'journals', None),
	# (u'children', None),
	# (u'custom_fields', [{u'id': 5, u'value': u'ES', u'name': u'Country'}]),
	# (u'description', u'Os paso el html.\r\n\r\nMuchas gracias'),
	# (u'changesets', None),
	# (u'watchers', None),
	# (u'author', {u'id': 159, u'name': u'David Clemente'}),
	# (u'created_on', u'2018-09-20T11:26:10Z'),
	# (u'relations', None),
	# (u'id', 64291),
	# (u'priority', {u'id': 5, u'name': u'Alta'}),
	# (u'tracker', {u'id': 2, u'name': u'Tareas'}),
	# (u'fixed_version', {u'id': 72, u'name': u'Sprint 2018-19'}),
	# (u'assigned_to', {u'id': 746, u'name': u'Carlos Mart\xednez'}),
	# (u'updated_on', u'2018-10-10T07:33:01Z'),
	# (u'subject', u'Cambiar Welcome de usuario duplicado en Salud Envidiable'),
	# (u'start_date', u'2018-09-20'), (u'done_ratio', 0)]

	#con issue.time_entries se saca el tiempo dedicado (te lo da por dias)

	#para sacar los datos de cada taquilla

	# for issue in issues:
	# 	#ticket - pais - proyecto - titulo
	# 	#print(list(issue))
	# 	print(issue.id, " - " , issue.custom_fields[0].value, " - " ,issue.project.name, " - " , issue.subject)

