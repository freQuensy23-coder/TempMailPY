import json
import re

import requests as r

from Exceptions import EmailNotSetError, IDNotSetError


class Fakemail:		#fakemail.net
	mainurl = 'https://www.fakemail.net/index/'

	def __init__(self, email=None):
		if email != None and email != '':
			self.setEmail(email)
		else:
			self.newEmail()

	def __del__(self):
		self.deleteEmail()

	def newEmail(self):
		self.sess = r.Session()
		self.email = None
		self.messinfo = []
		resp = self.sess.get(self.mainurl + 'index', headers={'X-Requested-With': 'XMLHttpRequest'}).text
		resp = json.loads(resp[1:])		#Decode response without the first char (server-side error)
		self.email = resp['email']

	def setEmail(self, email):	#Set custom email name
		if email == None or email == '':
			raise EmailNotSetError()
		self.sess = r.Session()
		self.email = None
		self.messinfo = []
		if '@' in email:
			email = email.split('@')[0]		#Split email by @ and only use the first part
		resp = self.sess.post(self.mainurl + 'new-email', data={'emailInput': email}, headers={'X-Requested-With': 'XMLHttpRequest'}).text
		if 'ok' in resp:
			self.email = email + '@aallaa.org'
		else:
			return 'ERROR|' + resp

	def getMessages(self):
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		resp = self.sess.post(self.mainurl + 'refresh', headers={'X-Requested-With': 'XMLHttpRequest'}).text
		resp = json.loads(resp[1:])
		self.messinfo = []
		for info in resp:
			self.messinfo.append([info['id'], re.findall('<(.*?)>', info['od'])[0], info['predmet']])	#Regex used to get only the email address
		return [self.messinfo, len(self.messinfo)]

	def getMessage(self, email_id):
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		if email_id == None or email_id == '':
			raise IDNotSetError()
		resp = self.sess.get(self.mainurl.replace('index', 'email') + 'id/' + str(email_id)).text
		return resp[1:]

	def getAll(self):
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		return [self.messinfo, len(self.messinfo)]

	def resetTime(self):	#Add 10 minutes
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		self.sess.get(self.mainurl.replace('index', 'expirace/600'))

	def deleteEmail(self):
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		self.sess.get(self.mainurl.replace('index', 'delete'))

	def getData(self):
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		return self.email