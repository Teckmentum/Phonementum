"""Modulos para conectarse a la base de datos

"""
import psycopg2
import global_settings as gv


def close_db_connection(cur, conn):
    # todo handler errors and posibles lost conenctions
    cur.close()
    conn.close()


def connect2django():
    """

    Returns:
        conn (psycopg2.connect): connection to PhonementumDB db
        cur: connection cursor

    """
    conn = psycopg2.connect(host=gv.postgres_host,
                            database=gv.postgres_database,
                            user=gv.postgres_user,
                            password=gv.postgres_password)
    cur = conn.cursor()

    return conn, cur
