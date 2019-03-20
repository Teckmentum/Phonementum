from hermes import hermes_helpers as hhelper
from db_manager import db_getters
import global_settings as gv
from twilio.twiml.voice_response import VoiceResponse, Gather, Say

HERMES_LIST_SITES = 'list_sites'


def list_sites(request):
    """
    This method get all sites for an umbrella company at the umbrella_sites_options,
    add the task to the session and set the twiml_xml.
    For this the method need the id for the company, entity_name='umbrella_sites'
    and the call_sid
    Args:
        request ():

    Returns:

    Notes:
        1. variables del task: maxTry, max_try_messg, is_gather, intro_msg, intro_voice_es
        2. este metodo solo esta funcionanda con espenol Todo en un futuro q se pueda seleccionar el idioma
    """
    result = hhelper.set_result(status=200)

    # get parameters
    parameters = hhelper.get_parameters(request=request,
                                        get_param=[gv.ID, gv.ENTITY_NAME],
                                        post_param=[gv.CALL_SID])
    # verify for missing parameters
    if parameters[gv.ERROR] is True:
        return parameters

    # get task from db and add it to session
    taskID = parameters[gv.ID] + HERMES_LIST_SITES
    if parameters[gv.CALL_SID] not in request.session.keys() or taskID not in request.session[parameters[gv.CALL_SID]].keys():
        parameters[gv.TASK_NAME] = HERMES_LIST_SITES
        result = hhelper.get_add_task(request, parameters, taskID)
        if result[gv.ERROR] is True:
            return result
    else:
        result[gv.MESSAGE] = 'task %s already in session for %s' % (taskID, parameters[gv.CALL_SID])

    # get sites from db
    sites = db_getters.get_values_from_hermes(get_values_id_name='task_id',
                                              table_name='umbrella_sites_options',
                                              get_values_id=taskID,
                                              column=['say_name_es', 'gather', 'say_voice_es'])
    if sites[gv.ERROR]:
        return sites


    # verify if task is gather and create the corresponding twiml_xml
    if request.session[parameters[gv.CALL_SID]][taskID][gv.TASK_VALUES][gv.IS_GATHER] == 'True':
        # calculate numDigits and range
        range_limit = len(sites[gv.FETCH])
        request.session[parameters[gv.CALL_SID]][taskID][gv.TASK_VALUES][gv.RANGE] = range_limit
        request.session[parameters[gv.CALL_SID]][taskID][gv.TASK_VALUES][gv.NUM_DIGITS] = len(str(range_limit)) # obtiene la cantidad de digitos en un numero

        # set gather action
        gather_action = gv.HOST + "/hermes/voice_call_gather?id=%s&entity_name=%s&taskname=%s" % (parameters[gv.ID], parameters[gv.ENTITY_NAME], HERMES_LIST_SITES)
        request.session[parameters[gv.CALL_SID]][taskID][gv.TASK_VALUES][gv.GATEHER_ACTION] = gather_action


        # set twilio response gather
        resp = VoiceResponse()
        gather = Gather(action=gather_action,
                        num_digits=request.session[parameters[gv.CALL_SID]][taskID][gv.TASK_VALUES][gv.NUM_DIGITS],
                        method='POST',
                        )

        # add the introduction mesg
        voice_intro_msg = request.session[parameters[gv.CALL_SID]][taskID][gv.TASK_VALUES]['intro_voice_es']
        intro_msg = request.session[parameters[gv.CALL_SID]][taskID][gv.TASK_VALUES]['intro_msg']
        gather.say(voice=voice_intro_msg, message=intro_msg)

        # add says for all sites
        # sites[gv.FETCH] contiene un array de tuplo cada tuplo contiene el (say, gather, say_name_es)
        for i in range(3): #todo ver como reducir este 3 * n big o
            for elements in sites[gv.FETCH]:  # todo esto se debe de cambiar a q los indices no sean puesto directo talvez una referencia de indices a otro array
                mensaje = elements[0]
                mensaje += ', oprima el ' + str(elements[1])
                gather.append(Say(voice=elements[2]).ssml_prosody(mensaje, rate='90%'))
                # gather.say(message= mensaje, voice=elements[2])

            # add pause
            gather.pause(length=3)

        resp.append(gather)
        request.session[parameters[gv.CALL_SID]][taskID][gv.TASK_VALUES]['option_not_recognized'] = resp.to_xml()

    else:
        # set twilio response gather
        resp = VoiceResponse()

        # add the introduction mesg
        voice_intro_msg = request.session[parameters[gv.CALL_SID]][taskID][gv.TASK_VALUES]['intro_voice_es']
        intro_msg = request.session[parameters[gv.CALL_SID]][taskID][gv.TASK_VALUES]['intro_msg']
        resp.say(voice=voice_intro_msg, message=intro_msg)

        # add says for all sites
        # sites[gv.FETCH] contiene un array de tuplo cada tuplo contiene el (say, gather, say_name_es)
        for elements in sites[
            gv.FETCH]:  # todo esto se debe de cambiar a q los indices no sean puesto directo talvez una referencia de indices a otro array
            mensaje = elements[0]
            mensaje += ', oprima el ' + str(elements[1])
            resp.say(message=mensaje, voice=elements[2])

        request.session[parameters[gv.CALL_SID]][taskID][gv.TASK_VALUES]['option_not_recognized'] = resp.to_xml()

    request.session.modified = True
    result[gv.TWILM_XML] = resp.to_xml()
    print(result[gv.TWILM_XML])
    return result


def get_nereast_location():
    pass




