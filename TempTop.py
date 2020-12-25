import random
import re

import requests as r

from Exceptions import EmailNotSetError, IDNotSetError


class TempTop: #tempmail.top
	mainurl = 'https://tempmail.top/'
	domains = ['tempmail.top', 'spambox.win', 'dispomail.win']

	def __init__(self, email=None, domain=None):
		if domain != None and 0 <= domain <= 2:
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

	def newEmail(self):
		self.sess = r.Session()
		self.email = None
		self.messinfo = []
		self.messcontent = []
		resp = self.sess.get(self.mainurl + 'user.php?user=').text
		self.email = resp

	def setEmail(self, email):
		self.sess = r.Session()
		self.email = None
		self.messinfo = []
		self.messcontent = []
		resp = self.sess.get(self.mainurl + 'user.php?user=' + email).text
		self.email = resp

	def getMessages(self):
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		resp = self.sess.get(self.mainurl + 'mail.php?unseen=0').text.replace('\n', '').replace('  ', '')	#Returns html, must be parsed with regex
		self.messinfo = []
		self.messcontent = []
		counter = 0
		for info in re.findall('class=\"subject\">(.*?)</div>', resp):
			self.messinfo.append([info, re.findall('class=\"tmail-email-sender float-left\">(.*?)</div>', resp)[counter]])
			self.messcontent.append([info, re.findall('class=\"body\">(.*?)</div>', resp)[counter]])
			counter+=1
		return [self.messinfo, len(self.messinfo)]

	def getMessage(self, email_subj):
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		if email_subj == None or email_subj == '':
			raise IDNotSetError()
		retvalue = None
		for message in self.messcontent:
			if message[0].replace(' ', '').lower() == email_subj.replace(' ', '').lower():	#Match passed subject with subject in the content-list
				retvalue = message[1]
				break
		return retvalue

	def getAll(self):
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		return [self.messinfo, len(self.messinfo)]

	def getData(self):	#Get email data
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		return self.email