# This library contains APIs of Temp-Mail services and allows you to use them
# All classes have almost the same structure
# @author XazkerBoy (https://github.com/XazkerBoy/)
#
# Methods:
# __init__() - Initialise class
#	@param email (optional) The first part of an email address before @
#	@param domain (optional, not everywhere) Address domain from the list (see class domains variable)
# newEmail() - Create random new email address. Used on class init without custom email set
# (not everywhere) setEmail() - Set custom email address. Used on class init with custom email set
#	@param email (optional) Custom address. In most cases only the part before @
# getMessages() - Get all messages
# getMessage() - Get message contents
#	@param email_id Id of the email which content has to be fetched
# getAll() - Quickly get all fetched messages without refreshing the whole list (ONLY ONES, THAT WERE ALREADY FETCHED)
# (not everywhere) deleteEmail() - Delete existing email address. Used on class destruction
# getData() - Get email data (sometimes also returns secret key for debugging)
# (not everywhere) resetTime() - Reset time to 10 minutes


