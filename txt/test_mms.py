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
        media_url= 'https://external-preview.redd.it/zIMk7pnM_V4jTQJj5QQ-POFZxhRZH4cI72jzHZw29G4.jpg?auto=webp&s=2b45b8c29b2dd8407ad9a907010edd05689c0c4a',
        to=peoples