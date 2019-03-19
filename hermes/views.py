from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from requests import status_codes

import global_settings as gv
from hermes import hermes_errors as herror
from hermes import hermes_helpers as hhelper
from db_manager import db_getters, validations as db_validation
# Create your views here.

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
    entity_name amd id tienen q estar en los query parameters
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

    """
    # get parameters
    parameters = hhelper.get_parameters(request, post_param=[gv.CALL_SID, gv.SELECTION], get_param=[gv.ENTITY_NAME, gv.TASK_NAME])

    # verify for get_and_validate_parameters errors
    if parameters[gv.ERROR]:
        return HttpResponse(parameters['message'], status=400)

    # validate relationship between entity and id
    validation = hhelper.validate_entity_id_relationship(parameters[gv.ENTITY_NAME], parameters[gv.ID])
    if validation[gv.ERROR] or not validation['isValid']:
        print(validation[gv.MESSAGE])
        return HttpResponse(validation[gv.MESSAGE], status=validation['status'])

    # VERIFY IF GATHER TASK for callerSID ALREADY IN HERMES_SESSION if not set
    taskID = parameters[gv.ID] + parameters[gv.TASK_NAME]
    if taskID not in request.session[parameters[gv.CALL_SID]].keys():
        # include gather task at session
        task_value = db_getters.get_task(task_name=gv.TASK_GATHER, id_value=parameters[gv.ID])

        hhelper.add_callsid_to_session(request=request, call_sid=parameters[gv.CALL_SID],id=taskID,value=task_value)
        request.session.modified = True

        # verify error in getting task
        if request.session[parameters[gv.CALL_SID]][taskID]['error']:
            respond_message = request.session[parameters[gv.CALL_SID]][taskID]['message']
            # remove task from session bc it contain errors
            del request.session[parameters[gv.CALL_SID]][taskID]
            print(respond_message)
            return HttpResponse(respond_message, status=400)

        request.session[parameters[gv.CALL_SID]][taskID]['tries'] = 1

    # validate gather selection within range
    if int(parameters[gv.SELECTION]) > request.session[parameters[gv.CALL_SID]][taskID]['var_values']['range']:
        # verify if tries are done
        if request.session[parameters[gv.CALL_SID]][taskID]['tries'] > request.session[parameters[gv.CALL_SID]][taskID]['var_values']['maxTry']:
            temp_response = request.session[parameters[gv.CALL_SID]][taskID]['var_values']['max_try_messg']
            del request.session[parameters[gv.CALL_SID]][taskID]
            return HttpResponse(temp_response)

        # increase tries and return option not recognized message
        request.session[parameters[gv.CALL_SID]][taskID]['tries'] += 1
        request.session.modified = True
        print(request.session[parameters[gv.CALL_SID]].keys())
        return HttpResponse(request.session[parameters[gv.CALL_SID]][taskID]['var_values']['option_not_recognized'])

    # get twiml_xml for selected option
    twiml_xml = db_getters.get_twiml_xml(compound_id=[parameters[gv.SELECTION], parameters[gv.ID]], get_twiml_table_name=hhelper.set_table_name(parameters[gv.ENTITY_NAME], 'options'))

    # verify for errors
    if twiml_xml['error']:
        print(twiml_xml)
        return HttpResponse(twiml_xml, status=400)

    return HttpResponse(twiml_xml['twiml_xml'])


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

    return HttpResponse("hola")



