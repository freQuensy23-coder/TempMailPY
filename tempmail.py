# MADE BY --- XAZKERBOY --- https://github.com/XazkerBoy/
# This library contains APIs of Temp-Mail services and allows you to use them
# All classes have almost the same structure
# __init__ - Initialise class. Parameters: (optional) email - name of the email before @. (optional) domain - domain index from the list
# newEmail() - create new email address
# (not everywhere) setEmail() - set custom email address. Parameters: email - name of the email (before @)
# getMessages() - get all (new) messages
# getAll() - get all messages. Sometimes function above displays only new messages, this one displays all. It also sometimes doesnt require additional requests
# getMessage() - get message contents. Parameters: email_id (email_subj) - id (sometimes subject) of the email
# (not everywhere) deleteEmail() - delete existing email address. Used on class destruction
# getData() - get email data (sometimes also returns secret key for debugging)
# (not everywhere) addTime() - add time (reset time to 10 minutes)
# MADE BY --- XAZKERBOY --- https://github.com/XazkerBoy/


import requests as r
import json
import re
import random
import string

class Guerilla:		#guerrillamail.com
	sess = r.Session()	#Session for all rquests
	mainurl = 'https://api.guerrillamail.com/ajax.php'	#API URL
	messages = []	#All recieved messages

	def __init__(self, email=None):		# Library init (email - custom name for mail)
		self.sess = r.Session()		#Clean up
		self.email = None
		self.sid_token = None
		self.newEmail()
		if email != None and email != '':
			self.setEmail(email)
		self.seq = '2'	#Set last message id to 2 (1 - welcome email, we dont want to see it)

	def __del__(self):	#Library destruct
		self.deleteEmail()
		self.sess = r.Session()
		self.email = None
		self.sid_token = None

	def newEmail(self):		#Create new email
		self.sess = r.Session()
		self.email = None
		self.sid_token = None
		self.messinfo = []
		resp = self.sess.post(self.mainurl, data={'f': 'get_email_address'}).json()		#Request email address
		self.email = resp['email_addr']	#Set got email
		self.sid_token = resp['sid_token']	#Set sid token (needed for all requests)

	def setEmail(self, email):	#Set custom email name
		if self.sid_token == None:
			raise Exception('sid_token not set!')
		if email == None or email == '':
			raise Exception('Email not set!')
		if '@' in email:
			email = email.split('@')[0]		#Split email by @ and only use the first part
		resp = self.sess.post(self.mainurl, data={'f': 'set_email_user', 'sid_token': self.sid_token, 'email_user': email}).json()
		self.email = resp['email_addr']
		self.sid_token = resp['sid_token']

	def getMessages(self):	#Get new messages
		if self.sid_token == None or self.sid_token == '':
			raise Exception('sid_token not set!')
		resp = self.sess.post(self.mainurl, data={'f': 'check_email', 'sid_token': self.sid_token, 'seq': self.seq}).json()
		messinfo = []	#New messages
		counter = 0
		for info in resp['list']:
			if counter == 0:
				self.seq = info['mail_id']	#set the sequence number to highest id (to avoid showing old emails)
				counter += 1

			self.messinfo.append([info['mail_id'], info['mail_from'], info['mail_subject']])		#Append new message
			self.messages.append([info['mail_id'], info['mail_from'], info['mail_subject']])	#Append new message to all 
		return [messinfo, int(resp['count'])]

	def getMessage(self, email_id):		#Get message body
		if self.sid_token == None or self.sid_token == '':
			raise Exception('sid_token not set!')
		if email_id == None or email_id == '':
			raise Exception('email_id not set!')
		resp = self.sess.post(self.mainurl, data={'f': 'fetch_email', 'sid_token': self.sid_token, 'email_id': email_id}).json()
		return [resp['mail_body'], resp['mail_timestamp']]

	def getAll(self):	#Get all messages
		if self.sid_token == None or self.sid_token == '':
			raise Exception('sid_token not set!')
		return self.messages

	def deleteEmail(self):	#Delete mail (on destruct)
		if self.sid_token == None or self.sid_token == '':
			raise Exception('sid_token not set!')
		self.sess.post(self.mainurl, data={'f': 'forget_me', 'sid_token': self.sid_token})

	def getData(self):	#Get email data
		if self.sid_token == None or self.sid_token == '':
			raise Exception('sid_token not set!')
		return [self.email, self.sid_token]

class Fakemail:		#fakemail.net
	sess = r.Session()
	mainurl = 'https://www.fakemail.net/index/'
	messinfo = []

	def __init__(self, email=None):
		self.sess = r.Session()
		self.email = None
		if email != None and email != '':
			self.setEmail(email)
		else:
			self.newEmail()

	def __del__(self):
		self.deleteEmail()
		self.sess = r.Session()
		self.email = None
		self.messinfo = []

	def newEmail(self):
		self.sess = r.Session()
		self.email = None
		self.messinfo = []
		resp = self.sess.get(self.mainurl + 'index', headers={'X-Requested-With': 'XMLHttpRequest'}).text
		resp = json.loads(resp[1:])		#Decode response without the first char (server-side error)
		self.email = resp['email']

	def setEmail(self, email):	#Set custom email name
		self.sess = r.Session()
		self.email = None
		messinfo = []
		if '@' in email:
			email = email.split('@')[0]		#Split email by @ and only use the first part
		resp = self.sess.post(self.mainurl + 'new-email', data={'emailInput': email}, headers={'X-Requested-With': 'XMLHttpRequest'}).text
		if 'ok' in resp:
			self.email = email + '@aallaa.org'
		else:
			raise Exception('Email not got!')

	def getMessages(self):
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		resp = self.sess.post(self.mainurl + 'refresh', headers={'X-Requested-With': 'XMLHttpRequest'}).text
		resp = json.loads(resp[1:])
		self.messinfo = []
		for info in resp:
			self.messinfo.append([info['id'], re.findall('<(.*?)>', info['od'])[0], info['predmet']])	#Regex used to get only the email address
		return [self.messinfo, len(self.messinfo)]

	def getMessage(self, email_id):
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		if email_id == None or email_id == '':
			raise Exception('email_id not set!')
		resp = self.sess.get(self.mainurl.replace('index', 'email') + 'id/' + str(email_id)).text
		return resp[1:]

	def addTime(self):	#Add 10 minutes
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		self.sess.get(self.mainurl.replace('index', 'expirace/600'))

	def getAll(self):
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		return self.messinfo

	def deleteEmail(self):
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		self.sess.get(self.mainurl.replace('index', 'delete'))

	def getData(self):
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		return self.email

class NADA:		#getnada.com
	sess = r.Session()
	mainurl = 'https://getnada.com/api/v1/'
	domains = ['getnada.com', 'abyssmail.com', 'boximail.com', 'clrmail.com', 'dropjar.com', 'getairmail.com', 'givmail.com', 'inboxbear.com', 'robot-mail.com', 'tafmail.com', 'vomoto.com', 'zetmail.com']	#Mail domains
	messinfo = []

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

	def getMessages(self):
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		resp = self.sess.get(self.mainurl + 'inboxes/' + self.email).json()
		self.messinfo = []
		for info in resp['msgs']:
			self.messinfo.append([info['uid'], info['fe'], info['s']])
		return [self.messinfo, len(self.messinfo)]

	def getMessage(self, email_id):
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		if email_id == None or email_id == '':
			raise Exception('email_id not set!')
		resp = self.sess.get(self.mainurl + 'messages/' + email_id).json()
		return [resp['html'], resp['text'], resp['r']]

	def getAll(self):
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		return self.messinfo

	def getData(self):
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		return self.email

class TenMMail:	#10minutemail.com
	sess = r.Session()
	mainurl = 'https://10minutemail.com/session/'
	messinfo = []
	messcontent = []	#Content of messages

	def __init__(self):
		self.sess = r.Session()
		self.email = None
		self.messinfo = []
		self.messcontent = []
		self.newEmail()

	def newEmail(self):		#Create new email
		self.sess = r.Session()
		self.email = None
		self.messinfo = []
		self.messcontent = []
		resp = self.sess.get(self.mainurl + 'address').json()
		self.email = resp['address']	#Set got email

	def getMessages(self):	#Get new messages
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		resp = self.sess.get(self.mainurl.replace('session', 'messages') + 'messagesAfter/0').json()
		self.messinfo = []	#New messages
		self.messcontent = []
		for info in resp:
			self.messinfo.append([info['id'], info['sender'], info['subject']])		#Append new message
			self.messcontent.append([info['id'], info['bodyPlainText'], info['bodyHtmlContent']])	#Append message id and its content
		return [self.messinfo, len(self.messinfo)]

	def getMessage(self, email_id):		#Get message body
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		if email_id == None or email_id == '':
			raise Exception('email_id not set!')
		retvalue = None
		for message in self.messcontent:
			if message[0] == email_id:
				retvalue = [message[1], message[2]]		#Return content of the message with specified id
				break
		return retvalue

	def addTime(self):
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		self.sess.get(self.mainurl + 'reset')

	def getAll(self):
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		return self.messinfo

	def getData(self):	#Get email data
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		return self.email

class TempTop: #tempmail.top
	sess = r.Session()
	mainurl = 'https://tempmail.top/'
	messinfo = []
	messcontent = []
	domains = ['tempmail.top', 'spambox.win', 'dispomail.win']

	def __init__(self, email=None, domain=None):
		self.sess = r.Session()
		self.email = None
		self.messcontent = []
		if domain != None and 0 <= domain <= 2:
			if email != None and email != '':
				if '@' in email:
					email = email.split('@')[0]
				self.setEmail(email + '@' + self.domains[domain])
			else:
				self.newEmail()
		else:
			if email != None and email != '':
				if '@' in email:
					email = email.split('@')[0]
				self.setEmail(email + '@' + random.choice(self.domains))
			else:
				self.newEmail()

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
		self.messcontent = []
		messinfo = []
		resp = self.sess.get(self.mainurl + 'user.php?user=' + email).text
		self.email = resp

	def getMessages(self):
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		resp = self.sess.get(self.mainurl + 'mail.php?unseen=0').text.replace('\n', '').replace('  ', '')	#Returns html, must be parsed with regex
		self.messinfo = []
		self.messcontent = []
		if resp == '':
			return [self.messinfo, len(self.messinfo)]
		counter = 0
		for info in re.findall('class=\"subject\">(.*?)</div>', resp):
			self.messinfo.append([info, re.findall('class=\"tmail-email-sender float-left\">(.*?)</div>', resp)[counter]])
			self.messcontent.append([info, re.findall('class=\"body\">(.*?)</div>', resp)[counter]])
			counter+=1
		return [self.messinfo, len(self.messinfo)]

	def getMessage(self, email_subj):
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		if email_subj == None or email_subj == '':
			raise Exception('email_subj not set!')
		retvalue = None
		for message in self.messcontent:
			if message[0].replace(' ', '').lower() == email_subj.replace(' ', '').lower():	#Match passed subject with subject in the content-list
				retvalue = message[1]
				break
		return retvalue

	def getAll(self):
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		return self.messinfo

	def getData(self):	#Get email data
		if self.email == None or self.email == '':
			raise Exception('Email not set!')
		return self.email

class PostShift:	#post-shift.ru
	sess = r.Session()
	mainurl = 'https://post-shift.ru/api.php'
	messinfo = []
	domains = ['post-shift.ru', 'postshift.ru']

	def __init__(self, email=None, domain=None):
		self.sess = r.Session()
		self.email = None
		if domain != None and 0 <= domain <= 1:
			if email != None and email != '':
				if '@' in email:
					email = email.split('@')[0]
				self.setEmail(email + '@' + self.domains[domain])
			else:
				self.newEmail()
		else:
			if email != None and email != '':
				if '@' in email:
					email = email.split('@')[0]
				self.setEmail(email + '@' + random.choice(self.domains))
			else:
				self.newEmail()

	def __del__(self):
		self.deleteEmail()
		self.sess = r.Session()
		self.email = None
		self.messinfo = []

	def newEmail(self):		#Create new email
		self.sess = r.Session()
		self.email = None
		self.key = None
		self.messinfo = []
		resp = self.sess.get(self.mainurl + '?action=new&type=json').json()
		self.email = resp['email']	#Set got email
		self.key = resp['key']

	def setEmail(self, email):	#Set custom email name
		self.sess = r.Session()
		self.email = None
		self.key = None
		messinfo = []
		resp = self.sess.get(self.mainurl + '?action=new&name=' + email.split('@')[0] + '&domain=' + email.split('@')[1] + '&type=json').json()
		self.email = resp['email']
		self.key = resp['key']

	def getMessages(self):
		if self.key == None or self.key == '':
			raise Exception('Key not set!')
		resp = self.sess.get(self.mainurl + '?action=getlist&key=' + self.key + '&type=json')
		self.messinfo = []
		if 'error' in resp.text:
			return [self.messinfo, len(self.messinfo)]
		resp = resp.json()
		if len(resp) == 0:
			return [self.messinfo, len(self.messinfo)]
		for info in resp:
			self.messinfo.append([info['id'], re.findall('<(.*?)>', info['from'])[0], info['subject']])
		return [self.messinfo, len(self.messinfo)]

	def getMessage(self, email_id):
		if self.key == None or self.key == '':
			raise Exception('Key not set!')
		if email_id == None or email_id == '':
			raise Exception('email_id not set!')
		resp = self.sess.get(self.mainurl + '?action=getmail&key=' + self.key + '&id=' + str(email_id) + '&type=json').json()
		return resp['message']

	def getAll(self):
		if self.key == None or self.key == '':
			raise Exception('Key not set!')
		return self.messinfo

	def addTime(self):
		if self.key == None or self.key == '':
			raise Exception('Key not set!')
		self.sess.get(self.mainurl + '?action=update&key=' + self.key)

	def deleteEmail(self):
		if self.key == None or self.key == '':
			raise Exception('Key not set!')
		self.sess.get(self.mainurl + '?action=clear&key=' + self.key)

	def getData(self):
		if self.key == None or self.key == '':
			raise Exception('Key not set!')
		return [self.email, self.key]