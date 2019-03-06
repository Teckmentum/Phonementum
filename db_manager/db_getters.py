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


def get_lobby_xml(to_number):
    #por el momento lo que hace es leer el xml en el directorio Fake_DB
    #return os.getcwd() + "\\Fake_DB\\" + to_number + ".xml"
    return to_number + ".xml"


def get_department_xml(to_number, department):
    return to_number + "_dept_" + department + ".xml"


def get_twiml_xml(id=None, table=None, phone=None, gather=None):
    """

    Args:
        id (): primary key of the table to connect
        table (str): table name to connect at the db
        phone (str): complete phone number without + sign

    Returns:
        dict: {'isValid': bool, 'error': str, 'status': int, 'twiml_xml': str}

    Notes:
        1. Author: Glorimar Castro-Noriega
        2. Date: 3-5-19
    """

    # validate id and table param, also gather is it is passed
    if gather is None:
        result = validations.validate_id_table(id=id, table_name=table)
    else:
        result = validations.validate_gather_id_table(id=id, table_name=table, gather=gather)

    if result['error'] is None and result['isValid']:
        # validate phone param
        if gather is None and phone is None:
            result['error'] = True
            result['messege'] = db_errors.ArgsCantBeNone('get_twiml_xml', 'id', 'table', 'phone or gather').message
        else:
            query_option = "gather = '%s'" % gather if gather is not None else "phone = '%s'" % phone.replace("+", "")
            query = "SELECT twiml_xml FROM phonementum.%s " \
                    "where %s = '%s' and %s" % (table, validations.ID_NAMES[table],
                                                id, query_option)
            conn, cur = connect.connect2django()

            cur.execute(query)
            result['twiml_xml'] = cur.fetchone()
            connect.close_db_connection(cur=cur, conn=conn)  # todo manejar errores en la coneccion del db

            # look at db

    # if twiml_xml is None element was not found
    if result['twiml_xml'] is None:
        result['error'] = True
        result['messege'] = "An element for the given id at the given table was not found"
        result['status'] = 400
    else:
        result['twiml_xml'] = result['twiml_xml'][0]  # fetchone return a tuple here we are selecting the real value

    print(result)
    # print(ET.tostring(result['twiml_xml'][0], encoding='utf8', method='xml'))

    return result


get_twiml_xml(id='660902047', table='company_options', gather='1')
