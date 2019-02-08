from django.shortcuts import render
from twilio.rest import Client
import global_settings as gv

# Create your views here.


client = Client(gv.twilio_sid, gv.twilio_token)


def make_call():
    pass
