from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather, Enqueue, Say
import global_settings as gv

client = Client(gv.twilio_sid, gv.twilio_token)

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

"""Redirect call to a sip endpoint
Description:
------------
    Este metodo recibe como query parametrs: domain and department.
    Depende del dominio y el departamento return un xml con instrucciones a que sip redirigir la llamada

Notes:
-------
    Author: Glorimar Castro
"""
@csrf_exempt
def sip_redirect(request):
    #request = (HttpRequest)(request)

    #get parametrs
    digits = None
    to = None
    domain = None
    department = None
    if request.method == "POST":
        digit       = request.POST.get("Digits")
        to          = request.POST.get("To")
        domain      = request.GET.get("domain")
        department  = request.GET.get("department")
    elif request.method == "GET":
        pass
    #return el xml adecuado dependiendo de los parametros
    print("devolviendo el file: " + to + "_dept_" + department + "_sel_" + digit + ".xml")
    return HttpResponse(open(to + "_dept_" + department + "_sel_" + digit + ".xml").read())

@csrf_exempt
def hold_xml(request):
    # ------------------------
    # extraer a quien se llama
    # ------------------------


    # buscar en la base de datos el xml de este numero

    # devolver el xml
    return HttpResponse(open("+18634003829_soporte_validacion.xml").read())