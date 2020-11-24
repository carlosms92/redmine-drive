from redminelib import Redmine
from datetime import date, timedelta
import sys

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

	# [
	# 	('relations', []), 
	# 	('time_entries', None), 
	# 	('children', None), 
	# 	('attachments', None), 
	# 	('changesets', None), 
	# 	('journals', None), 
	# 	('watchers', None), 
	# 	('id', 75141), 
	# 	('project', {'id': 134, 'name': 'Privacy'}), 
	# 	('tracker', {'id': 2, 'name': 'Tareas'}), 
	# 	('status', {'id': 5, 'name': 'Cerrada'}), 
	# 	('priority', {'id': 6, 'name': 'Urgente'}), 
	# 	('author', {'id': 490, 'name': 'Erika Elisabetta Montani'}), 
	# 	('assigned_to', {'id': 746, 'name': 'Carlos Martínez'}), 
	# 	('subject', 'URGENTE - log usuario sablex2011@libero.it'), 
	# 	('description', 'Hola \r\nnecesitamos el log de este usuario: sablex2011@libero.it\r\nMil gracias\r\nErika\r\n'), 
	# 	('start_date', '2020-10-29'), 
	# 	('due_date', None), 
	# 	('done_ratio', 0), 
	# 	('is_private', False), 
	# 	('estimated_hours', None), 
	# 	('created_on', '2020-10-29T16:40:38Z'), 
	# 	('updated_on', '2020-11-03T10:12:00Z'), 
	# 	('closed_on', '2020-11-03T09:59:36Z')
	# ]
	# [
	# 	('relations', []), 
	# 	('time_entries', None), 
	# 	('children', None), 
	# 	('attachments', None), 
	# 	('changesets', None), 
	# 	('journals', None), 
	# 	('watchers', None), 
	# 	('id', 75127), 
	# 	('project', {'id': 119, 'name': 'JobPortal'}), 
	# 	('tracker', {'id': 3, 'name': 'Soporte'}), 
	# 	('status', {'id': 3, 'name': 'Resuelta'}), 
	# 	('priority', {'id': 7, 'name': 'Inmediata'}), 
	# 	('author', {'id': 55, 'name': 'Marta Olariaga'}), 
	# 	('assigned_to', {'id': 746, 'name': 'Carlos Martínez'}), 
	# 	('subject', 'Añadir desarrollo para evitar bots en Landing AMP OE ES'), 
	# 	('description', 'Hola, dados los problemas que está teniendo la bbdd con email de bots, necesitamos añadir algún desarrollo que no permita que estos bots se registren en la landing AMP de ofertas de Oficina Empleo ES.\r\n\r\nOs dejo la url de ejemplo:https://jobs.oficinaempleo.com/ofertaempleoAMP?id=5472110\r\n\r\nEs bastante urgente porque OE está captando muchos registros y tenemos clientes que se están quejando.\r\n\r\nCualquier cosa nos decís. \r\nMil gracias! :)'), 
	# 	('start_date', '2020-10-28'), 
	# 	('due_date', None), 
	# 	('done_ratio', 0), 
	# 	('is_private', False), 
	# 	('estimated_hours', None), 
	# 	('custom_fields', [{'id': 5, 'name': 'Country', 'value': 'ES'}]), 
	# 	('created_on', '2020-10-28T13:04:04Z'), 
	# 	('updated_on', '2020-11-03T09:57:39Z'), 
	# 	('closed_on', '2020-11-03T09:57:39Z')
	# ]

	#con issue.time_entries se saca el tiempo dedicado (te lo da por dias)

	#para sacar los datos de cada taquilla

	# for issue in issues:
	# 	#ticket - pais - proyecto - titulo
	# 	#print(list(issue))
	# 	print(issue.id, " - " , issue.custom_fields[0].value, " - " ,issue.project.name, " - " , issue.subject)
