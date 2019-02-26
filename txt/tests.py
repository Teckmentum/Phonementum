from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
import global_settings as gv

# Your Account Sid and Auth Token from twilio.com/console
account_sid = gv.twilio_sid
auth_token = gv.twilio_token
client = Client(account_sid, auth_token)
people = ['+17872152776', '+17872459899','+17873929361']

for peoples in people:
   message = client.messages.create(
        body= "hey all you people, would you listen to me!",
        from_='+14154171040',
        to=peoples
    )

#message = client.messages \
               # .create(
               #      body="lo logre!",
               #      from_='+14154171040',
                #     to=people
                # )


print(message.sid)