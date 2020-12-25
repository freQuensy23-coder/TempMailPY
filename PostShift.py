import random
import re

import requests as r

from Exceptions import KeyNotSetError, IDNotSetError, EmailNotSetError


class PostShift:	#post-shift.ru
	mainurl = 'https://post-shift.ru/api.php'
	domains = ['post-shift.ru', 'postshift.ru']

	def __init__(self, email=None, domain=None):
		if domain != None and 0 <= domain <= 1:
			if email != None and email != '':
				if '@' in email:
					email = email.split('@')[0]
				status = self.setEmail(email + '@' + self.domains[domain])
			else:
				status = self.newEmail()
		else:
			if email != None and email != '':
				if '@' in email:
					email = email.split('@')[0]
				status = self.setEmail(email + '@' + random.choice(self.domains))
			else:
				status = self.newEmail()
		if status != None:
			raise Exception(status)

	def __del__(self):
		self.deleteEmail()

	def newEmail(self):		#Create new email
		self.sess = r.Session()
		self.email = None
		self.key = None
		self.messinfo = []
		resp = self.sess.get(self.mainurl + '?action=new&type=json').json()
		if 'error' in resp:
			return 'ERROR|' + resp['error']
		self.email = resp['email']	#Set got email
		self.key = resp['key']

	def setEmail(self, email):	#Set custom email name
		self.sess = r.Session()
		self.email = None
		self.key = None
		self.messinfo = []
		resp = self.sess.get(self.mainurl + '?action=new&name=' + email.split('@')[0] + '&domain=' + email.split('@')[1] + '&type=json').json()
		if 'error' in resp:
			return 'ERROR|' + resp['error']
		self.email = resp['email']
		self.key = resp['key']

	def getMessages(self):
		if self.key == None or self.key == '':
			raise KeyNotSetError()
		resp = self.sess.get(self.mainurl + '?action=getlist&key=' + self.key + '&type=json').json()
		if 'error' in resp:
			return 'ERROR|' + resp['error']
		self.messinfo = []
		if len(resp) == 0:
			return [self.messinfo, len(self.messinfo)]
		for info in resp:
			self.messinfo.append([info['id'], re.findall('<(.*?)>', info['from'])[0], info['subject']])
		return [self.messinfo, len(self.messinfo)]

	def getMessage(self, email_id):
		if self.key == None or self.key == '':
			raise KeyNotSetError()
		if email_id == None or email_id == '':
			raise IDNotSetError()
		resp = self.sess.get(self.mainurl + '?action=getmail&key=' + self.key + '&id=' + str(email_id) + '&type=json').json()
		return resp['message']

	def getAll(self):
		if self.key == None or self.key == '':
			raise KeyNotSetError()
		return [self.messinfo, len(self.messinfo)]

	def resetTime(self):
		if self.key == None or self.key == '':
			raise KeyNotSetError()
		self.sess.get(self.mainurl + '?action=update&key=' + self.key)

	def deleteEmail(self):
		if self.key == None or self.key == '':
			raise KeyNotSetError()
		self.sess.get(self.mainurl + '?action=clear&key=' + self.key)

	def getData(self):
		if self.key == None or self.key == '':
			raise KeyNotSetError()
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		return [self.email, self.key]