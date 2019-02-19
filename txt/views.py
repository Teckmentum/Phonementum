from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import global_settings as gv

from django.shortcuts import render

# Create your views here.
@csrf_exempt
def test(request):
    return HttpResponse("txt app working" + gv.twilio_num_etax_fl)