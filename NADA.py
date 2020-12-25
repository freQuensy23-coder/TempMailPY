import random

import requests as r

from Exceptions import EmailNotSetError, IDNotSetError


class NADA:		#getnada.com
	mainurl = 'https://getnada.com/api/v1/'
	domains = ['getnada.com', 'abyssmail.com', 'boximail.com', 'clrmail.com', 'dropjar.com', 'getairmail.com', 'givmail.com', 'inboxbear.com', 'robot-mail.com', 'tafmail.com', 'vomoto.com', 'zetmail.com']	#Mail domains

	def randomString(self, stringLength = 10):	#Random string generator
		letters = 'abcdefghijklmnopqrstuvwxyz'
		return ''.join([random.choice(letters) for n in range(stringLength)])

	def __init__(self, email=None, domain=None):
		self.sess = r.Session()
		self.email = None
		self.messinfo = []
		if domain != None and 0 <= domain <= 11:
			if email != None and email != '':
				if '@' in email:
					email = email.split('@')[0]
				self.email = email + '@' + self.domains[domain]		#If domain AND email are set
			else:
				self.email = self.randomString() + '@' + self.domains[domain]	#If only domain isset
		else:
			if email != None and email != '':
				if '@' in email:
					email = email.split('@')[0]
				self.email = email + '@' + random.choice(self.domains)	#If only email isset
			else:
				self.email = self.randomString() + '@' + random.choice(self.domains)	#If nothing isset

	def newEmail(self):
		self.sess = r.Session()
		self.email = None
		self.messinfo = []
		self.email = self.randomString() + '@' + random.choice(self.domains)

	def setEmail(self, email, domain = None):
		self.sess = r.Session()
		self.email = None
		self.messinfo = []
		if email == None or email == '':
			raise EmailNotSetError()
		if domain != None and 0 <= domain <= 11:
			if '@' in email:
				email = email.split('@')[0]
			self.email = email + '@' + self.domains[domain]
		else:
			if '@' in email:
				email = email.split('@')[0]
			self.email = email + '@' + random.choice(self.domains)

	def getMessages(self):
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		resp = self.sess.get(self.mainurl + 'inboxes/' + self.email).json()
		if 'error' in resp:
			return 'ERROR|' + resp['error']
		self.messinfo = []
		for info in resp['msgs']:
			self.messinfo.append([info['uid'], info['fe'], info['s']])
		return [self.messinfo, len(self.messinfo)]

	def getMessage(self, email_id):
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		if email_id == None or email_id == '':
			raise IDNotSetError()
		resp = self.sess.get(self.mainurl + 'messages/' + email_id).json()
		if 'error' in resp:
			return 'ERROR|' + resp['error']
		return [resp['html'], resp['text']]

	def getAll(self):
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		return [self.messinfo, len(self.messinfo)]

	def getData(self):
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		return self.email