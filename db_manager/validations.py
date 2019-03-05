import sys
sys.path.insert(0, '../../')
import re
from db_manager import db_errors

ALLOWED_TABLE_VALUES = {'company': r"^\d{9}$", 'department': r"^\d+$",
                        'site_dba': r"^\d{7}-\d{4}$",
                        'company_phone': r"^\d{9}$", 'department_phone': r"^\d+$",
                        'site_dba_phone': r"^\d{7}-\d{4}$"
                        }
ID_NAMES = {'company': 'ein', 'department': 'd_id',
            'site_dba': 'reg_comer',
            'company_phone': 'ein',
            'site_dba_phone': 'reg_comer'
            }

def validate_id_table(id=None, table_name=None):
    """
    Metodo valida que el id pasado sea del formato del primary key para
    la tabla que se intenta conectar en el db.
    Para la tabla de compania el id debe ser un ein (numero de 9 digitos).
    Para la tabla de site-dba el id debe ser una combinacion de 7digitos-4digitos.
    Para la tabla de department el id debe ser un entero.

    Args:
        id (str): Represent PrimaryKey for the specified table
        table_name (str): the table name from which id is going to be selected
    Returns:
        dict: {'isValid': bool, 'error': str, 'status': int}
    Notes:
        1. Author: Glorimar Castro-Noriega
        2. Date: 3-3-19
        3. If isValid is None then an error was rise
    Examples:
        validIdTable("660698757", "company")

    """

    result = {'isValid': None, 'error': None, 'status': None}

    # verify params are not None if param are None return a error: args cannot be None
    if id is None or table_name is None:
        result['error'] = db_errors.ArgsCantBeNone("validate_id_table", "id", "table").message
        result['status'] = 400
    # verify is table_name is valid and if id correspond to a primary key in table_name
    if table_name not in ALLOWED_TABLE_VALUES.keys():
        result['error'] = db_errors.InvalidArgValue(table_name, *ALLOWED_TABLE_VALUES.keys()).message
        result['status'] = 400
    else:
        result['isValid'] = True if re.match(ALLOWED_TABLE_VALUES[table_name], id) else False

    return result
