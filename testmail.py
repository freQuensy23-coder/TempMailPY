from tempmail import Guerilla, Fakemail, NADA, TenMMail, TempTop, PostShift

# mailclient = Guerilla()
# mailclient = Fakemail()
# mailclient = TenMMail()
# mailclient = TempTop()
# mailclient = PostShift()
mailclient = NADA()		#Init NADA client and get new mail address
print(mailclient.getData())		#Display mail address

while True:
	answer = input('[1] - New email address\r\n[2] - Check new (+old) messages\r\n[3] - Get all messages\r\nSelect action: ')
	if answer == '1':
		mailclient.newEmail()	#Get new mail address
		print(mailclient.getData())
	elif answer == '2':
		messages = mailclient.getMessages()	#Get messages
		print('Message count: ' + str(messages[1]))	#Print message count
		if(messages[1] > 0):
			for message in messages[0]:	#Display each message
				print('Message info:')
				print(message)
				print('Message body:')
				print(mailclient.getMessage(message[0]))
	elif answer == '3':
		messages = mailclient.getAll()	#Get all messages
		print('Message count: ' + str(len(messages)))
		if(len(messages) > 0):
			for message in messages:
				print('Message info:')
				print(message)
				print('Message body:')
				print(mailclient.getMessage(message[0]))