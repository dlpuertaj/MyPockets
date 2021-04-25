import mysql.connector
import sqlite3 as sql
from database import database_constants as const_db
from sqlite3 import Error as error_sqlite


class DatabaseManager:

    def __init__(self):
        self.database = const_db.DATABASE
        self.user = const_db.USER_DB
        self.password = const_db.PASSWORD_DB
        self.host = const_db.HOST_DB

    def create_connection(self, sqlite):
        connection = None
        try:

            if sqlite is True:
                connection = sql.connect(r"./" + self.database)
            else:
                connection = mysql.connector.connect(host=self.host,
                                                     database=self.database,
                                                     user=self.user,
                                                     password=self.password)

        except error_sqlite as e:
            print(e)

        return connection

    @staticmethod
    def execute_sqlite_query(conexion, query, values, multi):
        try:
            cursor = conexion.cursor()
            if values is not None:
                cursor.execute(query,values)
            else:
                cursor.execute(query)
            print("Query executed!")
        except error_sqlite as e:
            print(e)

        if multi:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()

        cursor.close()
        conexion.commit()

        return result

    @staticmethod
    def execute_mysql_query(conexion, query, values, multi):
        result = None
        try:
            cursor = conexion.cursor(buffered=True)

            if values is not None:
                cursor.execute(query, values, multi)
            else:
                cursor.execute(query, multi)

            if multi:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()

                conexion.conexion.commit()
            cursor.close()
            print(cursor.rowcount, "Query ejecutado con éxito!")
        except:
            print(cursor.rowcount, "Query ejecutado con errores!")

        return result
