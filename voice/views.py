from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from db_manager import db_getters
from django.views.decorators.csrf import csrf_exempt
import json

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

    #------------------------
    #extraer a quien se llama
    # ------------------------
    to_phone = None
    if request.method == 'POST':
        body = request.body.decode('utf-8') #body en django por defaul son byte
        print("primero")
        print(body)
        body = json.load(body)
        print("segundo")
        print(body)
        to_phone = body['To']
    elif request.method == 'GET':
        to_phone = str(request.GET.get('To')).strip()
    #buscar en la base de datos el xml de este numero
    print(to_phone)
    #devolver el xml
    return HttpResponse("hola")#open(db_getters.get_lobby_xml(to_phone) ).read())