from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt


import global_settings as gv
from hermes import hermes_errors as herror
from hermes import hermes_helpers as hhelper
from hermes import hermes_tasks as htask
from db_manager import db_getters

import json
# Create your views here.

"""
session = {callsid: {taskid:{var_values={},...}, taskid:{var_values={},...}}
           callsid: {taskid:{var_values={},...}, taskid:{var_values={}, gater_option={1: xml, 2:xml}}}
          }
"""
@csrf_exempt
def greetings(request):
    """
    This method is for testing. To test if the server is uo and running.

    Args:
        request (HttpRequest): it can be any http method

    Returns: a simple string saying hi.

    """
    return HttpResponse("Saludos mi nombre es Hermes y soy el IVR de Teckmentum")


@csrf_exempt
def incoming_voice_call_lobby(request):
    """
    This method extract from _phone table the twiml_xml value. To work it need
    entity_name, id, callsid and To. Callsid and To los provee twilio pero
    entity_name amd id tienen q estar en los query parameters.
    Args:
        request ():

    Returns:

    """

    # get parameters if a parameter is missing return an error
    parameters = hhelper.get_parameters(request, post_param=[gv.CALL_SID], get_param=[gv.ENTITY_NAME])
    if parameters[gv.ERROR]:
        print(parameters[gv.MESSAGE])
        return HttpResponse(parameters[gv.MESSAGE], status=parameters['status'])

    # validate relationship between entity and id
    validation = hhelper.validate_entity_id_relationship(parameters[gv.ENTITY_NAME], parameters[gv.ID])
    if validation[gv.ERROR] or not validation['isValid']:
        print(validation[gv.MESSAGE])
        return HttpResponse(validation[gv.MESSAGE], status=validation['status'])

    # get twiml_xml if error o no twiml was found reeturn error
    compound_id = hhelper.set_compound_id(entity_id=parameters[gv.ID], table_type_id=parameters[gv.TO])
    twiml_xml = db_getters.get_twiml_xml(compound_id=compound_id,
                                         get_twiml_table_name=hhelper.set_table_name(parameters[gv.ENTITY_NAME], 'phone'))
    if twiml_xml['error']:
        print(twiml_xml[gv.MESSAGE])
        return HttpResponse(twiml_xml[gv.MESSAGE], status=500)
    if twiml_xml['twiml_xml'] is None:
        print(twiml_xml)
        return HttpResponse(twiml_xml[gv.MESSAGE], status=400)

    # get twiml for after_lobby, table use is the entity table itself
    twiml_xml_after_lobby = db_getters.get_twiml_xml(get_twiml_id=parameters[gv.ID],
                                         get_twiml_table_name=parameters[gv.ENTITY_NAME])

    # add twiml after lobby at hermes session
    if not twiml_xml_after_lobby[gv.ERROR] and twiml_xml_after_lobby['twiml_xml'] is not None:
        hhelper.add_callsid_to_session(request=request, call_sid=parameters[gv.CALL_SID],
                               value=twiml_xml_after_lobby['twiml_xml'], id=gv.TWILIOML_AFTER_LOBBY)
    request.session.modified = True
    return HttpResponse(twiml_xml['twiml_xml'], status=200)


@csrf_exempt
def incoming_voice_call_from_lobby(request):

    # get parameters if one missing return error
    parameters = hhelper.get_parameters(request=request, post_param=[gv.CALL_SID])
    if parameters[gv.ERROR]:
        print(parameters[gv.MESSAGE])
        return HttpResponse(parameters[gv.MESSAGE], status=parameters['status'])

    # get twiml from hermessession
    if parameters[gv.CALL_SID] in request.session.keys() and gv.TWILIOML_AFTER_LOBBY in request.session[parameters[gv.CALL_SID]].keys():
        return HttpResponse(request.session[parameters[gv.CALL_SID]][gv.TWILIOML_AFTER_LOBBY])
    else:
        return HttpResponse("For %s and twiml after lobby wasnt found" % (parameters[gv.CALL_SID]), status=400)


@csrf_exempt
def incoming_voice_call_gather(request):
    """
    This method get an twiml_xml from an option table and return it. Gather method work only
    on _options table at hermes db. The request need to pass, callsid, to, id, entity_name, taskname.
    Funciona para cualquier task q necesite un gather, as long haya una tabala en el db taskname_options
    Args:
        request ():

    Returns:
    Notes:
        1. This method use te query parameter isLocal to decide where the gather options are going to be look up.
        if True then the gather option for the taskId have to be at request.session at [callsid][taskid][gather_options]
        if false then the gather option need to be in a table at the db with the table name been equal tu entityname_options
    """
    print('esta entrando en el area de gather')
    # get parameters
    parameters = hhelper.get_parameters(request, post_param=[gv.CALL_SID, gv.SELECTION], get_param=[gv.ENTITY_NAME, gv.TASK_NAME])
    parameters['isLocal'] = request.GET.get('isLocal') if request.GET.get('isLocal')is None else False

    # verify for get_and_validate_parameters errors
    if parameters[gv.ERROR]:
        return HttpResponse(parameters['message'], status=400)

    # validate relationship between entity and id
    validation = hhelper.validate_entity_id_relationship(parameters[gv.ENTITY_NAME], parameters[gv.ID])
    if validation[gv.ERROR] or not validation['isValid']:
        print(validation[gv.MESSAGE])
        return HttpResponse(validation[gv.MESSAGE], status=validation['status'])

    # VERIFY IF GATHER TASK for callerSID ALREADY IN HERMES_SESSION if not set
    # todo se deberia del mensaje de option not recognized cuando se vayan a repetir las opciones buscar si hay un
    # twiml after lobby y repetirlo
    taskID = parameters[gv.ID] + parameters[gv.TASK_NAME]
    if taskID not in request.session[parameters[gv.CALL_SID]].keys():
        result = hhelper.get_add_task(request=request, parameters=parameters, taskID=taskID)
        if result[gv.ERROR] is True:
            return HttpResponse(result, status=result['status'])

        request.session[parameters[gv.CALL_SID]][taskID]['tries'] = 1

    # validate gather selection within range
    if int(parameters[gv.SELECTION]) > request.session[parameters[gv.CALL_SID]][taskID]['var_values']['range']:
        # verify if tries are done
        if request.session[parameters[gv.CALL_SID]][taskID]['tries'] > request.session[parameters[gv.CALL_SID]][taskID]['var_values'][gv.MAX_TRIES]:
            temp_response = request.session[parameters[gv.CALL_SID]][taskID]['var_values'][gv.MAX_TRY_MESG]
            del request.session[parameters[gv.CALL_SID]][taskID]
            return HttpResponse(temp_response)

        # increase tries and return option not recognized message
        request.session[parameters[gv.CALL_SID]][taskID]['tries'] += 1
        request.session.modified = True
        print(request.session[parameters[gv.CALL_SID]].keys())
        return HttpResponse(request.session[parameters[gv.CALL_SID]][taskID]['var_values']['option_not_recognized'])

    # get twiml_xml for selected option
    twiml_xml = {}
    if parameters['isLocal'] == 'True':
        if 'gather_option' not in request.session[parameters[gv.CALL_SID]][taskID].keys():
            return HttpResponse('Gather is local  but there wasnt any gather_option for %s at session' % taskID)
        twiml_xml = request.session[parameters[gv.CALL_SID]][taskID]['gather_option'][parameters[gv.SELECTION]]
    else:
        twiml_xml = db_getters.get_twiml_xml(compound_id=[parameters[gv.SELECTION], parameters[gv.ID]], get_twiml_table_name=hhelper.set_table_name(parameters[gv.ENTITY_NAME], 'options'))

        # verify for errors
        if twiml_xml['error']:
            print(twiml_xml)
            return HttpResponse(twiml_xml, status=400)
        twiml_xml = twiml_xml['twiml_xml']

    # delete gatger task fo id at hermes session
    del request.session[parameters[gv.CALL_SID]][taskID]
    return HttpResponse(twiml_xml)


@csrf_exempt
def hermes_task(request, hermes_task=None):
    """
    This method start a hermes task. Each task do something different
    but all of them should return an xml. Refer to the task documentetion
    to see which variables are needed to pass and how to use them.
    Args:
        request ():
        hermes_task (): the hermes task to call

    Returns:

    """
    result = hhelper.set_result()

    if hermes_task == htask.HERMES_LIST_SITES:
        result = htask.list_sites(request)

    if result[gv.ERROR] is True:
        return HttpResponse(result[gv.MESSAGE], status=result[gv.STATUS])

    return HttpResponse(result[gv.TWILM_XML], status=200)



