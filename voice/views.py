from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from db_manager import db_getters
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather, Enqueue
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

@csrf_exempt
def enqueue_call(request):
    #request = (HttpRequest)(request)
    digit = None
    workflow = None
    task = None
    if request.method == 'POST':
        print("post")
        print(request.GET)
        digit       = request.POST.get("Digits")
        workflow    = request.POST.get("workflow")
        task        = request.POST.get("task")
    elif request.method == 'GET':
        print("get")
        print(request.GET)
        digit       = request.GET.get("Digits")
        workflow    = request.GET.get("workflow")
        task        = request.GET.get("task")

    task_json = {str(task):str(digit)}
    print(task_json)
    #resp = VoiceResponse()
    #enqueue = resp.enqueue(None, workflow_sid=gv.twilio_etaxes_workflow_sid[workflow])
    #enqueue.task(task_json)
    #resp.enqueue(enqueue)
    return HttpResponse("hola")