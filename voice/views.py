from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from db_manager import db_getters
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(reques):
    return HttpResponse("voice url working")
"""Manage incoming call to lobby

    Este app debe recibir las llamadas a Twilio identificar a que numero se estan tratando de comunicar y 
    devolver un xml que da las instrucciones para el numero que se estan tratando de comunicar
"""
@csrf_exempt
def incall_lobby(request):
    #request = (HttpRequest)(request)
    to_phone = None
    #recibir a quien se llama
    if request.method == 'POST':
        print(request.POST.keys())
        to_phone = request.body['To']
    elif request.method == 'GET':
        to_phone = str(request.GET.get('To')).strip()
    #buscar en la base de datos el xml de este numero
    print(to_phone)
    #devolver el xml
    return HttpResponse("hola")#open(db_getters.get_lobby_xml(to_phone) ).read())