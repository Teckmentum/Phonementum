from django.http import HttpResponse, HttpRequest
from db_manager import db_getters
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather, Enqueue, Say
import global_settings as gv
from voice.twilio2voice_handeler import voice_helpers
from xml.etree import cElementTree as ET


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
    if parameters['error'] is False:
        # get xml from db if id exist in table if not return error
        twiml_xml = db_getters.get_twiml_xml(parameters['id'], table=parameters['table'],
                                             phone=parameters['phone'])
        print(twiml_xml)
        if twiml_xml['error'] is True:
            response = HttpResponse(twiml_xml['messege'], status=twiml_xml['status'])
        else:
            print(twiml_xml['twiml_xml'])
            response = HttpResponse(twiml_xml['twiml_xml'])
    else:
        print(3)
        response = HttpResponse(parameters['messege'], status=parameters['status'])
    print(response)
    return response




