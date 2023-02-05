import sqlite3

from database import database_manager as db
from database import database_constants as db_constants
from sqlite3 import  OperationalError as db_op_error, DatabaseError as db_error, Error as sqlite_exception

from entities.expense_event import ExpenseEvent
from entities.generic_type import GenericType
from entities.income_event import IncomeEvent
from entities.pocket import Pocket
from entities.pocket_transaction import PocketTransaction


def get_database_connection():
    connection = None
    try:
        connection = db.create_connection(True)
    except sqlite_exception as e:
        print(e)

    return connection


def execute_query(db_connection, query, parameters, multiple_results):
    result = None
    try:
        result = db.execute_sqlite_query(db_connection, query,
                                         parameters, multiple_results)
    except sqlite_exception as e:
        print(e)

    return result


""" POCKETS """


def get_pockets(database_connection):
    pockets_result = execute_query(database_connection, db_constants.SELECT_POCKETS, None, True)
    pockets = []
    if pockets_result is not None:
        for pocket in pockets_result:
            pocket_instance = Pocket(pocket_id=pocket[0], name=pocket[1], amount=pocket[2])
            transactions_result = execute_query(database_connection,
                                                db_constants.SELECT_TRANSACTIONS_BY_POCKET_ID,
                                                (pocket_instance.get_id(),pocket_instance.get_id()), True)
            for transaction in transactions_result:
                transaction_inst = PocketTransaction('External Source' if transaction[0] is None else transaction[0],
                                                     transaction[1], transaction[2], transaction[3])
                pocket_instance.add_transaction(transaction_inst)
            pockets.append(pocket_instance)
        return pockets
    else:
        return None


def get_pocket_by_name(db_connection, pocket_name):
    result = execute_query(db_connection, db_constants.SELECT_POCKET_BY_NAME, (pocket_name,), False)
    if result is not None:
        return result
    else:
        return None


def update_pocket(db_connection, pocket_name, pocket_id):
    result = execute_query(db_connection, db_constants.UPDATE_POCKET_NAME_BY_ID, (pocket_name, pocket_id), False)
    if result is not None:
        return result
    else:
        return None


def update_pocket_amount(db_connection, pocket, amount):
    result = execute_query(db_connection, db_constants.UPDATE_POCKET_AMOUNT_BY_NAME, (amount, pocket), False)
    if result is not None:
        return result
    else:
        return None


def insert_pocket(db_connection, pocket_name, amount):
    result = execute_query(db_connection, db_constants.INSERT_POCKET, (pocket_name, amount), False)
    if result is not None:
        return result
    else:
        return None


def delete_pocket(db_connection, pocket_name):
    result = execute_query(db_connection, db_constants.DELETE_POCKET_BY_NAME, (pocket_name,), False)
    if result is not None:
        return result
    else:
        return None


""" TRANSACTIONS """

def insert_transaction(db_connection, transaction):
    result = execute_query(db_connection, db_constants.INSERT_TRANSACTION, (transaction.pocket_id,
                                                                            transaction.target_pocket_id,
                                                                            transaction.amount,
                                                                            transaction.transaction_date),
                           True)
    if result is not None:
        return result
    else:
        return None


def get_transactions_by_pocket_id(db_connection, pocket_id):
    result_set = execute_query(db_connection, db_constants.SELECT_TRANSACTIONS_BY_POCKET_ID, (pocket_id,), True)
    if result_set is not None:
        transactions = []
        for result in result_set:
            transaction = PocketTransaction(pocket_id=result[0],
                                            target_pocket_id=result[1],
                                            amount=result[4],
                                            transaction_date=result[5])
            transactions.append(transaction)

        return transactions
    else:
        return None


""" TYPES """

def get_income_types(database_connection):
    result = execute_query(database_connection, db_constants.GET_INCOME_TYPES, None, True)
    types = []
    if result is not None:
        for r in result:
            income_type = GenericType(r[0], r[1], r[2], 0)
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


def get_expense_type_by_id(db_connection, expense_id):
    result = execute_query(db_connection, db_constants.GET_EXPENSE_TYPE_BY_ID, (expense_id,), False)
    if result is not None:
        return result[0]
    else:
        return None


def insert_expense_type(db_connection, name, note):
    result = execute_query(db_connection, db_constants.INSERT_EXPENSE_TYPE, (name, note), False)
    if result is not None:
        return result[0]
    else:
        return None


def get_expenses_by_month(db_connection, month):
    result_set = execute_query(db_connection, db_constants.GET_EXPENSE_EVENTS_BY_MONTH, (month,), True)
    expense_events = []
    if result_set is not None:
        for rs in result_set:
            expense = ExpenseEvent(rs[0], rs[1], rs[2], rs[3], rs[4])
            expense_events.append(expense)
        return expense_events
    else:
        return None


def insert_income_type(db_connection, name, note):
    result = execute_query(db_connection, db_constants.INSERT_INCOME_TYPE, (name, note, 0), False)
    if result is not None:
        return result[0]
    else:
        return None


def get_incomes_by_month(db_connection, month):
    results = execute_query(db_connection, db_constants.GET_INCOME_EVENTS_BY_MONTH, (month,), True)
    income_events = []
    if results is not None:
        for rs in results:
            event = IncomeEvent(rs[0], rs[1], rs[2], rs[3], rs[5])
            income_events.append(event)
        return income_events
    else:
        return None


def get_event_types_by_event(db_connection, event_type):
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
def insert_event(db_connection, is_income, amount, event_type, date, note, pocket):
    if is_income:
        result = execute_query(db_connection, db_constants.INSERT_INCOME_EVENT,
                               (amount, event_type, date, note, pocket), False)
    else:
        result = execute_query(db_connection, db_constants.INSERT_EXPENSE_EVENT,
                               (amount, event_type, date, note, pocket), False)
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
