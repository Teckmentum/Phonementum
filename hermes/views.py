from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from requests import status_codes

import global_settings as gv
from hermes import hermes_errors as herror
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
    parameters = get_parameters(request, post_param=[gv.CALL_SID], get_param=[gv.ENTITY_NAME])
    if parameters[gv.ERROR]:
        print(parameters[gv.MESSAGE])
        return HttpResponse(parameters[gv.MESSAGE], status=parameters['status'])

    # validate relationship between entity and id
    validation = validate_entity_id_relationship(parameters[gv.ENTITY_NAME], parameters[gv.ID])
    if validation[gv.ERROR] or not validation['isValid']:
        print(validation[gv.MESSAGE])
        return HttpResponse(validation[gv.MESSAGE], status=validation['status'])

    # get twiml_xml if error o no twiml was found reeturn error
    compound_id = set_compound_id(entity_id=parameters[gv.ID], table_type_id=parameters[gv.TO])
    twiml_xml = db_getters.get_twiml_xml(compound_id=compound_id,
                                         get_twiml_table_name=set_table_name(parameters[gv.ENTITY_NAME], 'phone'))
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
        add_callsid_to_session(request=request, call_sid=parameters[gv.CALL_SID],
                               value=twiml_xml_after_lobby['twiml_xml'], id=gv.TWILIOML_AFTER_LOBBY)

    return HttpResponse(twiml_xml['twiml_xml'], status=200)


@csrf_exempt
def incoming_voice_call_from_lobby(request):

    # get parameters if one missing return error
    parameters = get_parameters(request=request, post_param=[gv.CALL_SID])
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
    on _options table at hermes db. The request need to pass, callsid, to, id, entity_name
    Args:
        request ():

    Returns:

    """
    # get parameters
    parameters = get_parameters(request, post_param=[gv.CALL_SID, gv.SELECTION], get_param=[gv.ENTITY_NAME])

    # verify for get_and_validate_parameters errors
    if parameters[gv.ERROR]:
        return HttpResponse(parameters['message'], status=400)

    # validate relationship between entity and id
    validation = validate_entity_id_relationship(parameters[gv.ENTITY_NAME], parameters[gv.ID])
    if validation[gv.ERROR] or not validation['isValid']:
        print(validation[gv.MESSAGE])
        return HttpResponse(validation[gv.MESSAGE], status=validation['status'])

    # VERIFY IF GATHER TASK for callerSID ALREADY IN HERMES_SESSION if not set
    taskID = parameters[gv.ID] + gv.TASK_GATHER
    if taskID not in request.session.get(parameters[gv.CALL_SID]).keys():
        # include gather task at session
        request.session[parameters[gv.CALL_SID]][taskID] = db_getters.get_task(task_name=gv.TASK_GATHER, id_value=parameters[gv.ID])

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
        print(request.session[parameters[gv.CALL_SID]][taskID]['tries'])
        print(request.session[parameters[gv.CALL_SID]][taskID]['var_values']['maxTry'])
        if request.session[parameters[gv.CALL_SID]][taskID]['tries'] >= request.session[parameters[gv.CALL_SID]][taskID]['var_values']['maxTry']:
            temp_response = request.session[parameters[gv.CALL_SID]][taskID]['var_values']['max_try_messg']
            del request.session[parameters[gv.CALL_SID]][taskID]
            return HttpResponse(temp_response)

        # increase tries and return option not recognized message
        request.session[parameters[gv.CALL_SID]][taskID]['tries'] += 1
        return HttpResponse(request.session[parameters[gv.CALL_SID]][taskID]['var_values']['option_not_recognized'])

    # get twiml_xml for selected option
    twiml_xml = db_getters.get_twiml_xml(compound_id=[parameters[gv.SELECTION], parameters[gv.ID]], get_twiml_table_name=set_table_name(parameters[gv.ENTITY_NAME], 'options'))

    # verify for errors
    if twiml_xml['error']:
        print(twiml_xml)
        return HttpResponse(twiml_xml, status=400)

    return HttpResponse(twiml_xml['twiml_xml'])


"""
HELPERS FUNCTIONS
"""


def get_parameters(request, get_param=[], post_param=[]):
    """
    Extrae por default id and To from an HttpRequest. Fuera de eso extrae to_do
    los parametros que se le pidan. Si uno de esos parametros  no es encontrado se devuelve un error
    Args:
        get_param:
        post_param:
        request ():
        *args ():

    Returns:

    """
    # request = HttpRequest(request)

    # get default parameters
    result = {'error': False, 'isValid': False, 'status': 200}
    result[gv.ID] = request.GET.get(gv.ID)
    result[gv.TO] = request.POST.get(gv.TO)[1:]

    # get extra parameters
    for element in post_param:
        result[element] = request.POST.get(element)
    for element in get_param:
        result[element] = request.GET.get(element)

    # verify for missing parameters
    if None in result.values():
        result[gv.ERROR]= True
        result['status']=400
        get_param_temp = ""
        print(result)
        for element in result.values():
            if element is None:
                get_param_temp += get_param_temp + ", "

        result[gv.MESSAGE]= herror.MissingParameterAtRequest(get_param_temp[0:-2]).message
        return result

    return result


def validate_entity_id_relationship(table_name=None, _id=None):
    """

    Args:
        table_name ():
        _id ():

    Returns:

    """
    result = set_result()
    # verify that a value was passed
    if table_name is None or _id is None:
        result[gv.ERROR: herror.MissingParameterAtRequest('entity_name', 'id').message]
        result['status'] = 500
        return result

    val_result = db_validation.validate_id_table_relationship(id=_id, table_name=table_name)

    # verify errors in validate relationship
    if val_result['error'] is True:
        return set_result(val_result[gv.MESSAGE], True, 400)

    # verify if not valid
    if val_result['isValid'] is False:
        result = set_result('Relationship between %s and %s is not valid' % (_id, table_name), True, 400)
        result['isValid'] = False
        return result

    # return values
    result['isValid'] = val_result['isValid']
    return result


def set_result(message=None, error=None, status=200, twiml_xml=None):
    """
    This method is just to ensure to always give as a result a dictionary with
    message, error, status, twiml_xml
    Args:
        message ():
        error ():
        status ():
        twiml_xml ():

    Returns:
        dict: dictionary {mesage, error, status, twiml_xml}

    """
    result = {gv.ERROR: error, gv.MESSAGE: message, 'status':status, 'twiml_xml':twiml_xml}
    return result


def set_table_name(entity_name, table_type):
    return entity_name + "_" + table_type


def set_compound_id(entity_id, table_type_id):
    return [table_type_id, entity_id]


def add_callsid_to_session(request, call_sid, id, value):
    """
    Add a key, value to HERMES_SESSION for call_sid
    Args:
        request:
        call_sid ():
        id ():
        value ():

    Returns:

    """
    if call_sid not in request.session.keys():
        request.session[call_sid] = {}

    request.session[call_sid][id] = value


