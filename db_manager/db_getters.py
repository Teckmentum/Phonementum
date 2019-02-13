"""Modulos paraz obtener data del db
"""
from os.path import dirname, realpath
import os
"""Modulo que devuelve el xml del lobby para el numero indicado en to_number


"""
def get_lobby_xml(to_number):
    #por el momento lo que hace es leer el xml en el directorio Fake_DB
    #return os.getcwd() + "\\Fake_DB\\" + to_number + ".xml"
    return to_number + ".xml"

def get_department_xml(to_number, department):
    return to_number + "_dept_" + department + ".xml"


#get_lobby_xml("+18634003829")