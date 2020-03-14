# TempMailPY
Collection of Temp Mail APIs in one library

# Used services
* https://guerrillamail.com
* https://fakemail.net
* https://getnada.com
* https://10minutemail.com
* https://tempmail.top
* https://post-shift.ru
# Usage
Import needed classes (in this case - NADA):
```
from tempmail import NADA
```

Initialise class:
```
mailclient = NADA()
```

And use class methods!
# Methods
* **newEmail()** - Create new email address. Uses on class init
* **setEmail()** - (not in every class) Set custom email address
* **getMessages()** - Get all (sometimes all) messages
* **getAll()** - Get all messages. This method does sometimes not require requests
* **getMessage()** - Get message content by ID (sometimes - subject)
* **deleteEmail()** - (not in every class) Delete email. Used on class destruction
* **getData()** - Get email data (sometimes also returns email-key for debug)
* **addTime()** - (not in every class) Extend time to 10 minutes
