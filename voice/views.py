from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from db_manager import db_getters
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
import global_settings as gv

client = Client(gv.twilio_sid, gv.twilio_token)
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
        to_phone = request.POST.get("To")
    elif request.method == 'GET':
        to_phone = str(request.GET.get('To')).strip()

    #buscar en la base de datos el xml de este numero


    #devolver el xml
    return HttpResponse(open(db_getters.get_lobby_xml(to_phone) ).read())

@csrf_exempt
def incall_department(request):
    # ------------------------
    # extraer a quien se llama
    # ------------------------
    to_phone = None
    if request.method == 'POST':
        print(request.POST)
        print(request.body)
        to_phone = request.POST.get("To")
        department_id = request.POST.get("Digits")
    elif request.method == 'GET':
        to_phone = str(request.GET.get('To')).strip()

    # buscar en la base de datos el xml de este numero

    # devolver el xml
    return HttpResponse(open(db_getters.get_department_xml(to_phone, department_id)).read())

@csrf_exempt
def assignment_callback(request):
    return HttpResponse({}, content_type="application/json")

@csrf_exempt
def create_task(request):
    print(gv.twilio_etaxes_workspace_sid + "         " + gv.twilio_etaxes_workflow_sid["soporte"])
    task = client.taskrouter.workspaces(gv.twilio_etaxes_workspace_sid).tasks.create(gv.twilio_etaxes_workflow_sid["soporte"], attributes="{'selected_soporte':'3'}")
    print(task.attributes)
    return HttpResponse({},content_type="application/json")