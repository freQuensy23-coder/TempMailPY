import requests as r

from Exceptions import EmailNotSetError, IDNotSetError


class TenMMail:	#10minutemail.com
	mainurl = 'https://10minutemail.com/session/'

	def __init__(self):
		status = self.newEmail()
		if status != None:
			raise Exception(status)

	def newEmail(self):		#Create new email
		self.sess = r.Session()
		self.email = None
		self.messinfo = []
		self.messcontent = []
		resp = self.sess.get(self.mainurl + 'address').json()
		self.email = resp['address']	#Set got email

	def getMessages(self):	#Get new messages
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		resp = self.sess.get(self.mainurl.replace('session', 'messages') + 'messagesAfter/0').json()
		self.messinfo = []	#New messages
		self.messcontent = []
		for info in resp:
			self.messinfo.append([info['id'], info['sender'], info['subject']])		#Append new message
			self.messcontent.append([info['id'], info['bodyPlainText'], info['bodyHtmlContent']])	#Append message id and its content
		return [self.messinfo, len(self.messinfo)]

	def getMessage(self, email_id):		#Get message body
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		if email_id == None or email_id == '':
			raise IDNotSetError()
		retvalue = None
		for message in self.messcontent:
			if message[0] == email_id:
				retvalue = [message[1], message[2]]		#Return content of the message with specified id
				break
		return retvalue

	def getAll(self):
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		return [self.messinfo, len(self.messinfo)]

	def resetTime(self):
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		self.sess.get(self.mainurl + 'reset')

	def getData(self):	#Get email data
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		return self.email