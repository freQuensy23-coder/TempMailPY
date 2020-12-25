# TempMailPY
Collection of Temp Mail APIs in one library

## Used services
* https://guerrillamail.com
* https://fakemail.net
* https://getnada.com
* https://10minutemail.com
* https://tempmail.top
* https://post-shift.ru
## Usage
Import needed classes (in this case - NADA):
```python
from NADA import NADA
```

Initialise class:
```python
mailclient = NADA()
```
(If an error occures while creating a new email address on init, en Exception will be thrown)

And use class methods!
## Methods
Name|Parameters|Description
--- | --- | ---
**newEmail()**||Create new email address. Uses on class init
**setEmail()**|email - custom address (in some cases only the part before @)|(not in every class) Set custom email address
**getMessages()**||Refresh message list and get it
**getAll()**||Get all already fetched messages. This method does not require requests
**getMessage()**|email_id (email_subj) - email ID (or, in some cases, subject) which content should be fetched|Get message content
**deleteEmail()**||(not in every class) Delete email. Used on class destruction
**getData()**||Get email data (sometimes also returns email-key for debug)
**resetTime()**||(not in every class) Reset time to 10 minutes
