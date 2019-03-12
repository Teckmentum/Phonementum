"""Modulos paraz obtener data del db
"""
import sys
sys.path.insert(0, '../../')
sys.path.insert(0, '../')
from db_manager import validations, db_connector as connect, db_errors
from xml.etree import cElementTree as ET
from psycopg2.extensions import new_type, register_type
import xml.dom.minidom as xmldom


# this methods are to cast xml data from postgres to python xml object

def get_values_from_hermes(get_values_id, table_name, column):
    """
    Get from the specified table at schema hermes the value of column where the Pk is get_values_id
    Args:
        get_values_id (str): PK at table_name
        table_name (str): name of the table to extract a value
        column (str): A specific column at table_name

    Returns:
        dic: if an error was rise the dic contain 'error' and 'message' if not is contain 'error' and column

    Notes:
        1. Author: Glorimar Castro-Noriega
    """
    result = {'error': False}

    # verify param values arent null
    if get_values_id is None or table_name is None or column is None:
        return {'error': True, 'message': db_errors.ArgsCantBeNone('get_values_from_hermes', 'id', 'table_name', 'column').message}

    # connect to db
    get_values_temp = connect.connect2django()

    if get_values_temp['error'] is True:
        return get_values_temp

    # verify table name is valid
    if table_name not in validations.ALLOWED_TABLE_VALUES.keys():
        return {'error': True, 'message': db_errors.DBError('%s is not a valid table name' % table_name)}

    # get value from db
    query = "select %s from hermes.%s where %s = '%s'" % (column, table_name,
                                                        validations.ID_NAMES[table_name], get_values_id)
    try:
        get_values_temp['cur'].execute(query)
        result[column] = get_values_temp['cur'].fetchone()
    except:
        return {'error': True, 'message': db_errors.DBError(message='An un expected error has ocurre at get_values_from_hermes')}
    finally:
        connect.close_db_connection(conn=get_values_temp['conn'], cur=get_values_temp['cur'])

    # verify that a value was found
    if result[column] is None:
        return {'error': True, 'message': db_errors.ValueNotFound(table_name=table_name, id=get_values_id, value_looked=column)}

    # set real result since fetchone return a tuple
    result[column] = result[column][0]
    return result


def get_twiml_xml(get_twiml_id=None, get_twiml_table_name=None):
    """
    Return the valuo at the column twiml_xml from the specified table_name where the pk is get_twiml_id
    Args:
        get_twiml_id (str):
        get_twiml_table_name (str):

    Returns:
        dic: if an error was rise the dic contain 'error' and 'message' if not is contain 'error' and column

    Notes:
        1. Author: Glorimar Castro-Noriega
    """
    # verify inputs are not None
    if get_twiml_id is None or get_twiml_table_name is None:
        return {'error': True, 'message': db_errors.ArgsCantBeNone('get_twiml_id', 'get_twiml_id', 'get_twiml_table_name')}

    return get_values_from_hermes(get_values_id=get_twiml_id, table_name=get_twiml_table_name,
                                            column='twiml_xml')


def get_task(id_value, task_name) -> dict:
    """

    Args:
        id_value (): 
        task_name (): 

    Returns:
        dict: 

    """
    if id_value is None or task_name is None:
        return {'error': True,
                'message': db_errors.ArgsCantBeNone('id_value', 'task_name')}

    # get task from hermes.task table
    return get_values_from_hermes(get_values_id=id_value + task_name, table_name='task', column='var_values')


