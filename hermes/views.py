from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from requests import status_codes

import global_settings as gv
from hermes import hermes_errors as herror
from db_manager import db_getters, validations as db_validation
# Create your views here.

HERMES_SESSION = {} # callerID: {taskID}


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
def incoming_voice_call_gather(request):
    # get parameters
    parameters = get_and_validate_parameters(request, gv.CALL_SID, gv.SELECTION)

    # verify for get_and_validate_parameters errtors
    if parameters['error'] or parameters['isValid'] is False:
        return HttpResponse(parameters['message'], status=400)

    # VERIFY IF GATHER TASK for callerSID ALREADY IN HERMES_SESSION if not set
    taskID = parameters[gv.ENTITY_ID] + gv.TASK_GATHER
    if parameters[gv.CALL_SID] not in HERMES_SESSION.keys():
        HERMES_SESSION[parameters[gv.CALL_SID]] = {}

    if taskID not in HERMES_SESSION.get(parameters[gv.CALL_SID]).keys():
        # include gather task at session
        HERMES_SESSION[parameters[gv.CALL_SID]][taskID] = db_getters.get_task(task_name=gv.TASK_GATHER, id_value=parameters['entity_id'])

        # verify error in getting task
        if HERMES_SESSION[parameters[gv.CALL_SID]][taskID]['error']:
            respond_message = HERMES_SESSION[parameters[gv.CALL_SID]][taskID]['message']
            # remove task from session bc it contain errors
            del HERMES_SESSION[parameters[gv.CALL_SID]][taskID]
            print(respond_message)
            return HttpResponse(respond_message, status=400)

        HERMES_SESSION[parameters[gv.CALL_SID]][taskID]['tries'] = 1

    # validate gather selection within range
    print(HERMES_SESSION)
    if int(parameters[gv.SELECTION]) > HERMES_SESSION[parameters[gv.CALL_SID]][taskID]['var_values']['range']:
        # verify if tries are done
        if HERMES_SESSION[parameters[gv.CALL_SID]][taskID]['tries'] == HERMES_SESSION[parameters[gv.CALL_SID]][taskID]['var_values']['maxTry']:
            temp_response = HERMES_SESSION[parameters[gv.CALL_SID]][taskID]['var_values']['max_try_messg']
            del HERMES_SESSION[parameters[gv.CALL_SID]][taskID]
            return HttpResponse(temp_response)

        # increase tries and return option not recognized message
        HERMES_SESSION[parameters[gv.CALL_SID]][taskID]['tries'] += 1
        return HttpResponse(HERMES_SESSION[parameters[gv.CALL_SID]][taskID]['var_values']['option_not_recognized'])

    # get twiml_xml for selected option
    twiml_xml = db_getters.get_twiml_xml(compound_id=parameters[gv.ID], get_twiml_table_name=parameters[gv.TABLE_NAME])

    # verify for errors
    if twiml_xml['error']:
        print(twiml_xml)
        return HttpResponse(twiml_xml, status=400)

    return HttpResponse(twiml_xml['twiml_xml'])


def get_and_validate_parameters(request, *args):
    # request = HttpRequest(request)

    # get default parameters
    result = {'error': False, 'isValid': False}
    result[gv.ID] = request.GET.get(gv.ID)
    result[gv.TABLE_NAME] = request.GET.get(gv.TABLE_NAME)
    result[gv.TO] = request.POST.get(gv.TO)

    # get extra parameters
    for element in args:
        result[element] = request.POST.get(element)

    # verify for missing parameters
    if None in result.values():
        return {'error': True, 'message': herror.MissingParameterAtRequest()}

    #verify if composite primary key, esto toma en cuenta que el id en el query solo representa un company, department or site_dba
    if '_options' in result[gv.TABLE_NAME] and gv.SELECTION in result.keys():
        result[gv.ENTITY_ID] = result[gv.ID]
        result[gv.ID] = '(%s, %s)' % (result[gv.SELECTION], result[gv.ID])
    elif '_phone' in result[gv.TABLE_NAME]:
        result[gv.ENTITY_ID] = result[gv.ID]
        result[gv.ID] = '(%s, %s)' % (result[gv.TO], result[gv.ID])
    val_result = db_validation.validate_id_table_relationship(id=result[gv.ID], table_name=result[gv.TABLE_NAME])

    # verify errors in validate relationship
    if val_result['error'] is True:
        return val_result

    # verify if not valid
    if val_result['isValid'] is False:
        return {'error': True, 'message': 'Relationship between %s and %s is not valid' % (result[gv.ID], result[gv.TABLE_NAME])}

    # return values
    result['isValid'] = val_result['isValid']
    return result


