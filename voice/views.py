from django.http import HttpResponse, HttpRequest
from db_manager import db_getters
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather, Enqueue, Say
import global_settings as gv
from voice.twilio2voice_handeler import voice_helpers
from xml.etree import cElementTree as ET

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
        to_phone = request.POST.get(gv.TO)
        department_id = request.POST.get(gv.SELECTION)
    elif request.method == 'GET':
        to_phone = str(request.GET.get(gv.TO)).strip()
        department_id = request.GET.get(gv.SELECTION)

    # buscar en la base de datos el xml de este numero

    # devolver el xml
    return HttpResponse(open(to_phone + "_dep_" + department_id + ".xml").read())

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

@csrf_exempt
def callUmbrellaCo(request):
    """
    Umbrella company es una compania que posee otras companias por lo que el mensaje
    que devuelve es uno que redirecciona a otros numeros de telefono

    Args:
        request (HttpRequest):

    Returns:

    Notes:
        1. Autor: Glorimar Castro-Noriega
        2. State: por el momento devuelve un xml hard coded debido a que no tenemos la base de datos ni los conectores

    """
    #request = (HttpRequest)(request)
    #variables a utilizar
    to_num      = None
    from_num    = None
    selection   = None
    timeout     = 20 #por default tendra 20 seg al menos q en la base de dato se muestre lo contrario
    company_name = "i-taxes"
    #obtener from, to
    if request.method == "GET":
        to_num = request.GET.get(gv.TO)
        from_num = request.GET.get(gv.FROM)
        selection = request.GET.get(gv.SELECTION)
        print("entro a get")
    elif request.method == "POST":
        print("entro a post")
        print(request.POST.dict())
        to_num = request.POST.get(gv.TO)
        from_num = request.POST.get(gv.FROM)
        selection = request.POST.get(gv.SELECTION)

    #manejar variables q no se le paso data
    if to_num == None or from_num == None or selection == None:
        #return error
        pass
    #si hay una seleccion redirigir a callCo()
    print("===============")
    print(selection)
    if selection != None:
        #las opciones aqui son temporeras en los que tenemos una base de  datos
        opciones = {
            "1": '+17872763490',
            "2": '+17872577459',#gv.twilio_num_etax_fl,
            "3": '+17872573957'
        }
        if selection == "1" or selection == "2" or selection == "3":
            return HttpResponse(open(opciones[selection] + ".xml").read())
        else:
            return HttpResponse(open("option_not_recognized.xml").read())
    #buscar en la base de dato cuales companias estan debajo de la umbrella

    #formar un xml q contenga un say que mencione las companias

    #devolver dicho xml/crear response

    return HttpResponse(open(to_num + ".xml").read())


"""
------------------------------------------------------------------------------
VOICE CALL HIERARCHY HANDLERS                    VOICE CALL HIERARCHY HANDLERS
------------------------------------------------------------------------------
"""

@csrf_exempt
def voice_call(request):
    """
    Return a xml with TwiML instructions for a Twilio call without gather.
    The xml is look up in the database for the table and id specified in
    the request. All incoming calls to twilio numbers create a request to this method.

    Args:
        request (HttpRequest): table and is params have to be at query request.
        At the Post body To need to be a param

    Returns:
        HttpResponse: if there wasnt any error it return a xml with twiml instruction for twilio

    Notes:
        1. Author: Glorimar Castro-Noriega
        2. Date: 3-5-19
    """

    parameters = {}
    response = None

    # get and validate parameters, also handle any error
    parameters = voice_helpers.extract_parameters(request)
    print(1)
    if parameters['error'] is False:
        print(2)
        # todo get and return xml
        # get xml from db if id exist in table if not return error
        twiml_xml = db_getters.get_twiml_xml(parameters['id'], table=parameters['table'], phone=parameters['phone'])
        print(twiml_xml)
        if twiml_xml['error'] is True:
            response = HttpResponse(twiml_xml['messege'], status=twiml_xml['status'])
        else:
            print(5)
            response = HttpResponse(twiml_xml['twiml_xml'][0])
    else:
        print(3)
        response = HttpResponse(parameters['messege'], status=parameters['status'])
    print(response)
    return response




