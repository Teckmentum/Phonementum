# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpRequest
from twilio.twiml.messaging_response import MessagingResponse


@csrf_exempt
def sms_reply(request):
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message("Ahoy! Thanks so much for your message, arrrgh.")

    return HttpResponse(resp)



