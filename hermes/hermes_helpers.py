import global_settings as gv
from hermes import hermes_errors as herror
from django.http import HttpRequest
from db_manager import db_getters, validations as db_validation


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
    result = set_result(message="", status=200, twiml_xml="")
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

        for element in result.keys():
            if result[element] is None:
                get_param_temp += element + ", "

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


def set_result(message=None, error=False, status=200, twiml_xml=None):
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


def get_add_task(request: HttpRequest, parameters: dict, taskID: str) -> dict:
    """
    Look for a task in the task table and added to the hermes session

    Args:
        request (HttpRequest):
        parameters (dict): {callsid, task_name, id } need to be at parameters
        taskID (str):

    Returns:
        dict: {error: bool, status: int, messege: str}


    """
    # todo si no estan todas las variables q el task no necesita se deberia tirar un error
    result = set_result(error=False, status=200)

    # include gather task at session
    task_value = db_getters.get_task(task_name=parameters[gv.TASK_NAME], id_value=parameters[gv.ID])
    add_callsid_to_session(request=request, call_sid=parameters[gv.CALL_SID],id=taskID,value=task_value)
    request.session.modified = True

    # verify error in getting task
    if request.session[parameters[gv.CALL_SID]][taskID]['error']:
        result = request.session[parameters[gv.CALL_SID]][taskID]
        result[gv.STATUS] = 400
        # remove task from session bc it contain errors
        del request.session[parameters[gv.CALL_SID]][taskID]
        return result

    return result



def hermes_redirect_call(phone_number: int = None, task_values: dict = None) -> object:
    """
    el metofo pregunta al usuario si quiere ser redireccionado si dice que no el metodo
    le cuelga. Si dice q si lo manda a un numero de telefono o sip
    Args:
        phone_number: numero de telefono donde se redireccionara la llamada
        task_values: diccionario que debe de cotener redirect_msg y goodbye_msg

    Returns:

    """
    # set result
    result = set_result()

    # verify if funtion parameters are valid:
    if phone_number is None:
        result[gv.MESSAGE] = herror.MissingParameterAtRequest('phone_number')
        result[gv.gv.ERROR] = True
        result[gv.gv.STATUS] = 500
    if 'redirect_msg' not in task_values.keys():
        result[gv.MESSAGE] = herror.MissingParameterAtRequest('redirect_msg')
        result[gv.gv.ERROR] = True
        result[gv.gv.STATUS] = 500
    if 'goodbye_msg' not in task_values.keys():
        result[gv.MESSAGE] = herror.MissingParameterAtRequest('goodbye_msg')
        result[gv.gv.ERROR] = True
        result[gv.gv.STATUS] = 500

    # preguntar si quiere ser redireccionado


def gather():
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
        if request.session[parameters[gv.CALL_SID]][taskID]['tries'] > \
                request.session[parameters[gv.CALL_SID]][taskID]['var_values']['maxTry']:
            temp_response = request.session[parameters[gv.CALL_SID]][taskID]['var_values']['max_try_messg']
            del request.session[parameters[gv.CALL_SID]][taskID]
            return HttpResponse(temp_response)

        # increase tries and return option not recognized message
        request.session[parameters[gv.CALL_SID]][taskID]['tries'] += 1
        request.session.modified = True
        print(request.session[parameters[gv.CALL_SID]].keys())
        return HttpResponse(request.session[parameters[gv.CALL_SID]][taskID]['var_values']['option_not_recognized'])


"end of file"
