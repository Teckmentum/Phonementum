import sys
sys.path.append('../')
from django.shortcuts import render
from twilio.rest import Client
import global_settings as gv
from twilio.twiml.voice_response import VoiceResponse, Gather

# Create your views here.


client = Client(gv.twilio_sid, gv.twilio_token)


def make_call():
    # Your Account Sid and Auth Token from twilio.com/user/account
    client = Client(gv.twilio_sid, gv.twilio_token)

    call = client.calls.create(
        to      ="+17872152776",
        from_   = gv.twilio_num_etax_fl,
        url     ="http://www.e-taxes.us/e-taxes.us/gcastro/voice_test.xml"
    )

    print(call.sid)

def voice():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()

    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            resp.say('You selected sales. Good for you!')
            return str(resp)
        elif choice == '2':
            resp.say('You need support. We will help!')
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say("Sorry, I don't understand that choice.")

    # Start our <Gather> verb
    gather = Gather(num_digits=1)
    gather.say('For sales, press 1. For support, press 2.')
    resp.append(gather)

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect('/voice')

    return str(resp)

make_call()
