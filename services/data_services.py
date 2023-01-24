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
        result = db.execute_sqlite_query(db_connection, query,
                                         parameters, multiple_results)
    except eqlite_exception as e:
        print(e)

    return result


""" POCKETS """
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

def get_pocket_by_name(db_connection, pocket_name):
    result = execute_query(db_connection, db_constants.SELECT_POCKET_BY_NAME, (pocket_name,),False)
    if result is not None:
        return result
    else:
        return None

def update_pocket(db_connection, pocket_name, pocket_id):
    result = execute_query(db_connection, db_constants.UPDATE_POCKET_NAME_BY_ID,(pocket_name, pocket_id),False)
    if result is not None:
        return result
    else:
        return None


def update_pocket_amount(db_connection, pocket,amount):
    result = execute_query(db_connection, db_constants.UPDATE_POCKET_AMOUNT_BY_NAME,(amount,pocket),False)
    if result is not None:
        return result
    else:
        return None

def insert_pocket(db_connection,pocket_name,amount):
    result = execute_query(db_connection, db_constants.INSERT_POCKET,(pocket_name,amount),False)
    if result is not None:
        return result
    else:
        return None

def delete_pocket(db_connection, pocket_name):
    result = execute_query(db_connection, db_constants.DELETE_POCKET_BY_NAME,(pocket_name,),False)
    if result is not None:
        return result
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
    result = execute_query(db_connection, db_constants.GET_EXPENSE_TYPES, None, True)
    types = []
    if result is not None:
        for r in result:
            expense_type = GenericType(r[0], r[1], r[2])
            types.append(expense_type)
        return types
    else:
        return None


def insert_expense_type(db_connection, name, note):
    result = execute_query(db_connection, db_constants.INSERT_EXPENSE_TYPE, (name, note), False)
    if result is not None:
        return result[0]
    else:
        return None


def insert_income_type(db_connection, name, note):
    result = execute_query(db_connection, db_constants.INSERT_INCOME_TYPE, (name, note), False)
    if result is not None:
        return result[0]
    else:
        return None


def get_events_by_type(db_connection, event_type):
    result = None
    type_of_event = str(type(event_type))
    if "expense" in type_of_event:
        result = execute_query(db_connection, db_constants.GET_EXPENSE_TYPES, None, True)
    elif "income" in type_of_event:
        result = execute_query(db_connection, db_constants.GET_INCOME_TYPES, None, True)
    types = []
    for r in result:
        generic_type = GenericType(r[0], r[1], r[2])
        types.append(generic_type)
    return types


# TODO: insert event using event object
def insert_event(db_connection, is_income, amount,event_type, date, note, pocket):
    if is_income:
        result = execute_query(db_connection, db_constants.INSERT_INCOME_EVENT,
                               (amount,event_type, date, note, pocket), False)
    else:
        result = execute_query(db_connection, db_constants.INSERT_EXPENSE_EVENT,
                               (amount,event_type, date, note, pocket), False)
    if result is not None:
        return result
    else:
        return None


""" RESUME data """
def get_resume_data_by_month(db_connection, month):
    result = execute_query(db_connection, db_constants.GET_EXPENSE_SUM_BY_TYPE_AND_MONTH, (month,), True)

    if result is not None:
        if len(result) == 0:
            return [('None', 0)]
        return result
    else:
        return None


def get_payroll_by_month(db_connection, month):

    result = execute_query(db_connection, db_constants.GET_PAYROLL_BY_MONTH, (month,), False)

    if result is not None:
        if len(result) == 0:
            return 0
        return result
    else:
        return 0

def verify_user_for_login(db_connection, username, password):
    result = execute_query(db_connection, db_constants.SEARCH_USER_BY_USERNAME_AND_PASSWORD,
                           (username, password), False)
    return result
