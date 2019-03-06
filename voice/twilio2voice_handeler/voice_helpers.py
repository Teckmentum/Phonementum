from django.http import HttpResponse, HttpRequest
from db_manager import validations as db_v
import global_settings as gv


def extract_parameters(request):
    """
    Method extract id, table and phone number from an HttpRequest.
    If a value is missing or their are not valid error
    is set tu True  and a status and message will be return.
    Args:
        request (HttpResponse): request object to a voice url

    Returns:
        dict: {'id': str, 'table': str, 'phone': str, 'gather': int
              'error': bool, 'status': int,
              'message': str}

    Notes:
        1. request method has to be a post method not a get
        2. Extrae phone, id and table. The phone is at the Post Body but the id and table have to be at the query parameters.
        3. gather is optional
    """
    #request = HttpRequest (request)
    result = {'id': None, 'table': None, 'phone': None, 'gather': None,
              'error': False, 'status': None,
              'message': None}


    # verify method is post
    if request.method == 'POST':
        # verify id and table are at query params and To at post body
        get_keys = request.GET.keys()
        if 'id' in get_keys and 'table' in get_keys and gv.TO in request.POST.keys():
            # set values
            result['id'] = request.GET.get('id')
            result['table'] = request.GET.get('table')
            result['phone'] = request.POST.get(gv.TO)
            result['gather'] = request.POST.get(gv.SELECTION)

            # validate id-table relationship
            validate_result = db_v.validate_id_table(result['id'], result['table'],
                                                     result['gather'])
            if not validate_result['isValid']:
                result['error'] = True
                result['status'] = 400
                result['message'] = "The id passed is not a primary key for the specified table"
            elif validate_result['isValid'] is None:
                result['error'] = True
                result['status'] = validate_result['status']
                result['message'] = validate_result['error']
        else:
            # return missing value
            result['error'] = True
            result['status'] = 400
            result['message'] = 'Parameters id, table and To are required. id and table are query parameters. To is a body parameter.'
    else:
        # respond http error 405, bc method is not post
        result['error'] = True
        result['status'] = 405
        result['message'] = 'Request method should be POST'

    return result
