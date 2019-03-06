"""Modulos paraz obtener data del db
"""
import sys
sys.path.insert(0, '../../')
sys.path.insert(0, '../')
from db_manager import validations, db_connector as connect, db_errors
from xml.etree import cElementTree as ET
from psycopg2.extensions import new_type, register_type
import xml.dom.minidom as xmldom


"""Modulo que devuelve el xml del lobby para el numero indicado en to_number


"""


# this methods are to cast xml data from postgres to python xml object
def cast_xml(value, cur):
    if value is None:
        return None
    return ET.fromstring(value)


register_type(new_type((142,), "XML", cast_xml))


def get_lobby_xml(to_number):
    #por el momento lo que hace es leer el xml en el directorio Fake_DB
    #return os.getcwd() + "\\Fake_DB\\" + to_number + ".xml"
    return to_number + ".xml"


def get_department_xml(to_number, department):
    return to_number + "_dept_" + department + ".xml"


def get_twiml_xml(id=None, table=None, phone=None):
    """

    Args:
        id (): primary key of the table to connect
        table (str): table name to connect at the db
        phone (str): complete phone number without + sign

    Returns:
        dict: {'isValid': bool, 'error': str, 'status': int, 'twiml_xml': str}
    """

    # validate id and table param
    result = validations.validate_id_table(id=id, table_name=table)
    if result['error'] is None and result['isValid']:
        #validate phone param
        if phone is not None:
            query = "SELECT twiml_xml FROM phonementum.%s where %s = '%s' and phone = '%s'" % (table,
                                                                                               validations.ID_NAMES[table],
                                                                                               id, phone.replace("+", ""))
            conn, cur = connect.connect2django()

            cur.execute(query)
            result['twiml_xml'] = cur.fetchone()
            connect.close_db_connection(cur=cur, conn=conn) # todo manejar errores en la coneccion del db
        else:
            result['error'] = True
            result['messege'] = db_errors.ArgsCantBeNone('get_twiml_xml', 'id', 'table', 'phone').message
        # look at db

    # if twiml_xml is None element was not found
    if result['twiml_xml'] is None:
        result['error'] = True
        result['messege'] = "An element for the given id at the given table was not found"
        result['status'] = 400

    #print(result)
    #print(ET.tostring(result['twiml_xml'][0], encoding='utf8', method='xml'))

    return result


#get_twiml_xml('0031765-0048', 'site_dba_phone', '17877860324')
