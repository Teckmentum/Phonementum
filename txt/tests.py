
from twilio.rest import Client
import global_settings as gv

# Your Account Sid and Auth Token from twilio.com/console
account_sid = gv.twilio_sid
auth_token = gv.twilio_token
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Hola hermosa~",
                     from_='+14154171040',
                     to='+17872459899'
                 )

print(message.sid)