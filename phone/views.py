from django.shortcuts import render
from twilio.rest import Client


# Create your views here.

#variables para auth con Twilio
account_sid     = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
auth_token      = 'your_auth_token'
client          = Client(account_sid, auth_token)


def make_call():
    pass
