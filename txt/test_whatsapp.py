import global_settings as gv
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
account_sid = gv.twilio_sid
auth_token = gv.twilio_token
client = Client(account_sid, auth_token)


message = client.messages.create(
                          body='Hello there!{{1}} espero que te ayan gustado los stitch, love {{2}}',
                          from_='whatsapp:+14155238886',
                          to='whatsapp:+17872459899'
                      )

print(message.sid)