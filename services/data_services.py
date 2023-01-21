from database import database_manager as db
from database import database_constants as db_constants
from sqlite3 import Error as eqlite_exception

from entities.generic_type import GenericType
from entities.pocket import Pocket


def get_database_connection():
    connection = None
    try:
        connection = db.create_connection(True)
    except eqlite_exception as e:
        print(e)

    return connection

def execute_query(db_connection, query, parameters, multiple_results):
    result = None
    try:
        result = db.execute_sqlite_query(db_connection,
                                         query,
                                         parameters,
                                         multiple_results)
    except eqlite_exception as e:
        print(e)

    return result

def get_pockets(database_connection):
    result_set = execute_query(database_connection, db_constants.SELECT_POCKETS, None, True)
    pockets = []
    if result_set is not None:
        for result in result_set:
            pocket = Pocket(pocket_id=result[0], name=result[1], amount=result[2])
            pockets.append(pocket)
        return pockets
    else:
        return None

def get_income_types(database_connection):

    result = execute_query(database_connection, db_constants.GET_INCOME_TYPES, None, True)
    types = []
    if result is not None:
        for r in result:
            income_type = GenericType(r[0], r[1], r[2])
            types.append(income_type)
        return types
    else:
        return None

def get_expense_types(db_connection):
    result = execute_query(db_connection,db_constants.GET_EXPENSE_TYPES, None, True)
    types = []
    if result is not None:
        for r in result:
            expense_type = GenericType(r[0], r[1], r[2])
            types.append(expense_type)
        return types
    else:
        return None