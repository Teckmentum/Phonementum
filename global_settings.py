"""File para inicializar las variables globales

Variables de token se deben inicializar aqui

"""

import os

"""
Temp session
"""
session = {} # for a temp global session

"""
TWILIO VARIABLES
"""
TWILIO_SID      = os.environ["twilio_sid"]
TWILIO_TOKEN    = os.environ["twilio_token"]
#twilio_etaxes_workspace_sid = os.environ["twilio_workspace_etaxes_sid"]
#twilio_etaxes_workflow_sid  = {"soporte": os.environ["twilio_etaxes_workflow_soporte"], "ventas": os.environ["twilio_etaxes_workflow_ventas"]}

"""
PHONE NUMBERS
"""
twilio_num_etax_fl  = "+18634003829"
twilio_num_etax_ne  = "+14023829377"


HOST = "https://phonementum.herokuapp.com"

"""
TWILIO BODY PARAMETERS
"""
TO          = "To"
FROM        = "From"
SELECTION   = "Digits"
ID          = 'id'
TABLE_NAME  = 'table_name'
CALL_SID    = 'CallSid'
ENTITY_NAME = 'entity_name'

TWILIOML_AFTER_LOBBY = 'twiml_after_lobby'
TWILM_XML = 'twiml_xml'

"""
TASK NAMES
"""
TASK_GATHER = 'gather'
ENTITY_ID = 'entity_id'
TASK_NAME = 'taskname'
IS_GATHER = 'is_gather'
INTRO_MSG = 'intro_msg'
TASK_VALUES = 'var_values'
RANGE = 'range'
FETCH = 'fetch'
GATEHER_ACTION = 'gather_action'
NUM_DIGITS = 'numDigits'

"""
TASK DICTIONARY KEYS NAMES
"""
MAX_TRY_MESG = 'max_try_messg'
GOODBYE_MSG = 'goodbye_msg'
REDIRECT_MSG = 'redirect_msg'

MESSAGE = 'message'
ERROR = 'error'
STATUS = 'status'



"""
POSTGRESS DB
"""
postgres_host = os.environ["postgres_host"]
postgres_database = os.environ["postgres_database"]
postgres_user = os.environ["postgres_user"]
postgres_password = os.environ["postgres_password"]
