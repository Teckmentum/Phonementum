import global_settings as gv
from hermes import hermes_errors as herror
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

