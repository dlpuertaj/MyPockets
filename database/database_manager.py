import mysql.connector
import sqlite3 as sql
from database import database_constants as db_const
from sqlite3 import Error as db_error


def create_connection(sqlite):
    connection = None
    try:

        if sqlite is True:
            connection = sql.connect(r"./" + db_const.DATABASE)
        else:
            connection = mysql.connector.connect(host=db_const.HOST_DB,
                                                 database=db_const.DATABASE,
                                                 user=db_const.USER_DB,
                                                 password=db_const.PASSWORD_DB)

    except db_error as e:
        print(e)

    return connection


def execute_sqlite_query(connection, query, values, multi):
    cursor = None
    try:
        cursor = connection.cursor()
        if values is not None:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
    except db_error as e:
        print(e)

    if multi:
        result = cursor.fetchall()
    else:
        result = cursor.fetchone()

    cursor.close()
    connection.commit()

    return result


def execute_mysql_query(connection, query, values, multi):
    result = None
    try:
        cursor = connection.cursor(buffered=True)

        if values is not None:
            cursor.execute(query, values, multi)
        else:
            cursor.execute(query, multi)

        if multi:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()

            connection.conexion.commit()
        cursor.close()
    except:
        print(cursor.rowcount, "Error executing query!")

    return result
