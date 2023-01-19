from database import database_manager as db
from database import database_constants as db_constants
from sqlite3 import Error as eqlite_error

def get_database_connection():
    connection = None
    try:
        connection = db.create_connection(True)
    except eqlite_error as e:
        print(e)

    return connection

def execute_query(query, parameters, multiple_results):
    connection = None
    try:
        connection = get_database_connection()
        result = db.execute_sqlite_query(connection, query, parameters, multiple_results)
    except eqlite_error as e:
        print(e)
    finally:
        if connection is not None:
            connection.close()

    return result