import sys
sys.path.insert(0, '../../')
import re
from db_manager import db_errors

ALLOWED_TABLE_VALUES = {'phone': r"^\d{11,15}$",
                        'company': r"^\d{9}$",
                        'department': r"^[\w-]{1,19}$",
                        'site_dba': r"^\d{7}-\d{4}$",
                        'company_phone': r"^\(\w{11,15}, \w{9}\)$",
                        'department_phone': r"^\(\d{11,15}, [\w-]{1,19}\)$",
                        'site_dba_phone': r"^\(\d{11,15}, \d{7}-\d{4}\)$",
                        'company_options': r"^\(\d+, \d{9}\)$",
                        'site_dba_options': r"^\(\d+, \d{7}-\d{4}\)$",
                        'department_options': r"^\(\d+, [\w-]{1,19}\)$",
                        'task': r"^[w ]{1,50}$",
                        'test': r"^\d+$"
                        }
ID_NAMES = {'company': 'ein',
            'department': 'd_id',
            'site_dba': 'reg_comer',
            'company_phone': '(phone, ein)',
            'site_dba_phone': '(phone, reg_comer)',
            'department_phone': '(phone, d_id',
            'company_options': '(gather, c_ein)',
            'department_options': '(gather, d_id)',
            'site_dba_options': '(gather, reg_comerciante)',
            'test': 'test_id',
            'task': 'task_id'
            }


def validate_id_table_relationship(id=None, table_name=None):
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
        dict: {'isValid': bool, 'error': str, 'message': str}
    Notes:
        1. Author: Glorimar Castro-Noriega
        2. Date: 3-3-19
        3. If isValid is None then an error was rise
    Examples:
        validIdTable("660698757", "company")

    """

    result = {'isValid': None, 'error': None}

    # verify params are not None if param are None return a error: args cannot be None
    if id is None or table_name is None:
        result['error'] = True
        result['message'] = db_errors.ArgsCantBeNone("validate_id_table", "id", "table").message

    # verify is table_name is valid and if id correspond to a primary key in table_name
    if table_name not in ALLOWED_TABLE_VALUES.keys():
        result['error'] = True
        result['message'] = db_errors.InvalidArgValue(table_name, *ALLOWED_TABLE_VALUES.keys()).message

    else:
        result['isValid'] = True if re.match(ALLOWED_TABLE_VALUES[table_name], id) else False

    return result


