import psycopg2
import global_settings as gv
"""
def insertPhone(county_code, area_code, subscriber_num, foward = None, twiml_xml = None):

    insert_sql = "insert into phonementum.phone(phone, county_code, area_code, subscriber_num) values (%d%d%d, %d, %d, %d)" % (county_code, area_code, subscriber_num, county_code, area_code, subscriber_num)
    if foward is not None and twiml_xml is not None:
        insert_sql = "insert into phonementum.phone(phone, county_code, area_code, subscriber_num, foward, twiml_xml) values (%d%d%d, %d, %d, %d, %d, XMLPARSE(DOCUMENT %s))" % (
        county_code, area_code, subscriber_num, county_code, area_code, subscriber_num, foward, twiml_xml)
    elif foward is not None:
        insert_sql = "insert into phonementum.phone(phone, county_code, area_code, subscriber_num, foward) values (%d%d%d, %d, %d, %d, %d)" % (
            county_code, area_code, subscriber_num, county_code, area_code, subscriber_num, foward)
    elif twiml_xml is not None:
        insert_sql = "insert into phonementum.phone(phone, county_code, area_code, subscriber_num, twiml_xml) values (%d%d%d, %d, %d, %d, XMLPARSE(DOCUMENT %s))" % (
            county_code, area_code, subscriber_num, county_code, area_code, subscriber_num, twiml_xml)

    conn = connect2django()
    cur = conn.cursor()
    cur.execute(insert_sql)
    conn.commit()
    cur.close()
    conn.close()
"""



def connect2django():
    conn = psycopg2.connect(host= gv.postgres_host,
                            database=gv.postgres_database,
                            user=gv.postgres_user,
                            password=gv.postgres_password)
    cur = conn.cursor()

    return conn, cur

#insertPhone(1, 787, 2459899)
#end of file