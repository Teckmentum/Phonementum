"""File para inicializar las variables globales

Variables de token se deben inicializar aqui

"""

import os

"""
TWILIO VARIABLES
"""
twilio_sid      = os.environ["twilio_sid"]
twilio_token    = os.environ["twilio_token"]
#twilio_etaxes_workspace_sid = os.environ["twilio_workspace_etaxes_sid"]
#twilio_etaxes_workflow_sid  = {"soporte": os.environ["twilio_etaxes_workflow_soporte"], "ventas": os.environ["twilio_etaxes_workflow_ventas"]}

"""
PHONE NUMBERS
"""
twilio_num_etax_fl  = "+18634003829"
twilio_num_etax_ne  = "+14023829377"




"""
TWILIO BODY PARAMETERS
"""
TO          = "To"
FROM        = "From"
SELECTION   = "Digits"
ID          = 'id'
TABLE_NAME  = 'table_name'
CALL_SID    = 'CallSid'

"""
TASK NAMES
"""
TASK_GATHER = 'gather'

ENTITY_ID = 'entity_id'



"""
POSTGRESS DB
"""
postgres_host = os.environ["postgres_host"]
postgres_database = os.environ["postgres_database"]
postgres_user = os.environ["postgres_user"]
postgres_password = os.environ["postgres_password"]
