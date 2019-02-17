from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from db_manager import db_getters
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather, Enqueue
import global_settings as gv
import urllib.parse

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
        to_phone = request.POST.get("To")
        department_id = request.POST.get("Digits")
    elif request.method == 'GET':
        to_phone = str(request.GET.get('To')).strip()
        department_id = request.GET.get("Digits")

    # buscar en la base de datos el xml de este numero

    # devolver el xml
    return HttpResponse(open(db_getters.get_department_xml(to_phone, department_id)).read())

@csrf_exempt
def assignment_callback(request):
    #request = (HttpRequest)(request)
    print("---------------------------------------------------------------")
    if request.method == "GET":
        print(request.GET)
    elif request.method == "POST":
        print(request.POST)
    print("---------------------------------------------------------------")
    return HttpResponse({}, content_type="application/json")

@csrf_exempt
def create_task(request):
    print(gv.twilio_etaxes_workspace_sid + "         " + gv.twilio_etaxes_workflow_sid["soporte"])
    task = client.taskrouter.workspaces(gv.twilio_etaxes_workspace_sid).tasks.create(workflow_sid=gv.twilio_etaxes_workflow_sid["soporte"], attributes='{"selected_soporte":"3"}')
    print(task.attributes)
    return HttpResponse({},content_type="application/json")

@csrf_exempt
def accept_reservation(request):
    #request = (HttpRequest)(request)
    #get task sid and reservation sid
    if request.method == 'GET':
        task_sid = request.GET.get("task_sid")
        reservation_sid = request.GET.get("reservation_sid")
    elif request.method == "POST":
        task_sid = request.POST.get("task_sid")
        reservation_sid = request.POST.get("reservation_sid")

    reservation = client.taskrouter.workspaces(gv.twilio_etaxes_workspace_sid)\
                    .tasks(task_sid).reservations(reservation_sid)\
                    .update(reservation_status='accepted')
    print(reservation.reservation_status)
    return HttpResponse({}, content_type="application/json")


"""Enqueue a selected task
Description:
-------------
    Este metodo se encarga de crear un task para TaskRouter y 
    lo manda a queue con el workflow indicado

Notes:
-------------
    Author:  Glorimar
    Created: Feb-13-2019
"""
@csrf_exempt
def enqueue_call(request, workspace, workflow, task_attributes):
    #request = (HttpRequest)(request)
    print("Working in workspace:" + workspace + " workflow: " + workflow)

    #get user selection
    digit = None
    if request.method == 'POST':
        digit = request.POST.get("Digits")
    elif request.method == 'GET':
        digit = request.GET.get("Digits")

    #set task attributes
    task_json = '{"' + task_attributes + '":"' + str(digit) + '"}'

    #enqueue task
    resp = VoiceResponse()
    enqueue = resp.enqueue(None, workflow_sid=gv.twilio_etaxes_workflow_sid[workflow], wait_url="http://phonementum.herokuapp.com/voice/hold")
    enqueue.task(task_json)
    resp.append(enqueue)
    return HttpResponse(str(resp))

@csrf_exempt
def retrun_mp3():
    #file = open("/path/to/my/song.mp3", "rb").read()
    #response['Content-Disposition'] = 'attachment; filename=filename.mp3'
    #return HttpResponse(file, mimetype="audio/mpeg")
    pass

@csrf_exempt
def sip_redirect(request):
    #request = (HttpRequest)(request)
    if request.method == "POST":
        print(request.POST)
    elif request.method == "GET":
        print(request.GET)
    return HttpResponse(open("test.xml").read())

@csrf_exempt
def hold_xml(request):
    # ------------------------
    # extraer a quien se llama
    # ------------------------


    # buscar en la base de datos el xml de este numero

    # devolver el xml
    return HttpResponse(open("+18634003829_soporte_validacion.xml").read())
