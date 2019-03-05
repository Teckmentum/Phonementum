import sys
sys.path.insert(0, '../../')
import re
from db_manager import db_errors

ALLOWED_TABLE_VALUES = {'company': r"^\d{9}$", 'department': r"^\d+$", 'site_dba': r"^\d{7}-\d{4}$"}


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
        dict: {'isValid': bool, 'error': str}
    Raises:
        ArgsCantBeNone: raised exception is id or table is None
        InvalidArgValue: raised if table value is not a valid one
    Notes:
        Author: Glorimar Castro-Noriega
        Date: 3-3-19
    Examples:
        validIdTable("660698757", "company")

    """

    result = {'isValid': None, 'error': None}

    # verify params are not None if param are None return a error: args cannot be None
    if id is None or table_name is None:
        raise db_errors.ArgsCantBeNone("validate_id_table", "id", "table")
        #todo devolver este error en el dict
    # verify is table_name is valid and if id correspond to a primary key in table_name
    if table_name not in ALLOWED_TABLE_VALUES.keys():
        result['error'] = db_errors.InvalidArgValue(table_name, *ALLOWED_TABLE_VALUES.keys()).message
    else:
        result['isValid'] = True if re.match(ALLOWED_TABLE_VALUES[table_name], id) else False

    print(result)
    return result


validate_id_table(table_name="department", id="667845988dd")
