import requests as r

from Exceptions import EmailNotSetError, IDNotSetError


class Guerilla:		#guerrillamail.com
	mainurl = 'https://api.guerrillamail.com/ajax.php'	#API URL

	def __init__(self, email=None):		# Library init (email - custom name for mail)
		status = self.newEmail()
		if status != None:
			raise Exception(status)
		if email != None and email != '':
			status = self.setEmail(email)
			if status != None:
				raise Exception(status)
		self.seq = '2'	#Set last message id to 2 (1 - welcome email, we dont want to see it)

	def __del__(self):	#Library destruct
		self.deleteEmail()

	def newEmail(self):		#Create new email
		self.sess = r.Session()		#New requests session
		self.email = None	#Clear email address
		self.sid_token = None	#Clear sid_token (needed for auth)
		self.messinfo = []	#Clear messages list
		resp = self.sess.post(self.mainurl, data={'f': 'get_email_address'}).json()		#Request email address
		if 'error' in resp:
			return 'ERROR|' + resp['error']
		self.email = resp['email_addr']	#Set got email
		self.sid_token = resp['sid_token']	#Set sid token (needed for all requests)

	def setEmail(self, email):	#Set custom email name
		if self.sid_token == None:
			return 'ERROR|TOKEN_NOT_SET';
		if email == None or email == '':
			raise EmailNotSetError()
		if '@' in email:
			email = email.split('@')[0]		#Split email by @ and only use the first part
		resp = self.sess.post(self.mainurl, data={'f': 'set_email_user', 'sid_token': self.sid_token, 'email_user': email}).json()
		if 'error' in resp:
			return 'ERROR|' + resp['error']
		self.email = resp['email_addr']
		self.sid_token = resp['sid_token']

	def getMessages(self):	#Get new messages
		if self.sid_token == None or self.sid_token == '':
			return 'ERROR|TOKEN_NOT_SET'
		resp = self.sess.post(self.mainurl, data={'f': 'check_email', 'sid_token': self.sid_token, 'seq': self.seq}).json()
		if 'error' in resp:
			return 'ERROR|' + resp['error']
		counter = 0
		for info in resp['list']:
			if counter == 0:
				self.seq = info['mail_id']	#set the sequence number to highest id (to avoid showing old emails)
				counter += 1
			self.messinfo.append([info['mail_id'], info['mail_from'], info['mail_subject']])	#Append new message to all
		return [self.messinfo, len(self.messinfo)]

	def getMessage(self, email_id):		#Get message body
		if self.sid_token == None or self.sid_token == '':
			return 'ERROR|TOKEN_NOT_SET'
		if email_id == None or email_id == '':
			raise IDNotSetError()
		resp = self.sess.post(self.mainurl, data={'f': 'fetch_email', 'sid_token': self.sid_token, 'email_id': email_id}).json()
		if 'error' in resp:
			return 'ERROR|' + resp['error']
		return resp['mail_body']

	def getAll(self):	#Get all fetched messages
		if self.sid_token == None or self.sid_token == '':
			return 'ERROR|TOKEN_NOT_SET'
		return [self.messinfo, len(self.messinfo)]

	def deleteEmail(self):	#Delete mail (on destruct)
		if self.sid_token == None or self.sid_token == '':
			return 'ERROR|TOKEN_NOT_SET'
		self.sess.post(self.mainurl, data={'f': 'forget_me', 'sid_token': self.sid_token})

	def getData(self):	#Get email data
		if self.sid_token == None or self.sid_token == '':
			return 'ERROR|TOKEN_NOT_SET'
		if self.email == None or self.email == '':
			raise EmailNotSetError()
		return [self.email, self.sid_token]