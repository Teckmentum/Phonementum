from hermes import hermes_helpers as hherlper
import global_settings as gv

HERMES_TASK = {'list_sites'}


def list_sites(request):
    result = hherlper.get_parameters(request=request,
                                     get_param=[gv.ID],
                                     post_param=[gv.CALL_SID])


def get_nereast_location():
    pass




