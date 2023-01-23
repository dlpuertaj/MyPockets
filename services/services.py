from database import database_constants as db_constants
from sqlite3 import Error as error_sqlite

from entities.expense_event import ExpenseEvent
from entities.income_event import IncomeEvent
from entities.pocket import Pocket
from frames.popup.popup_options_message import PopupOptionsMessage
from database import database_manager as db_manager

class Services:

    def __init__(self):
        self.is_logged_in = False

    def connect_and_execute(self, query, data, multi):
        connection = None
        try:
            connection = db_manager.create_connection(True)
            result = db_manager.execute_sqlite_query(connection,
                                                          query,
                                                          data,
                                                          multi)
        except error_sqlite as e:
            print(e)
        finally:
            if connection is not None:
                connection.close()

        return result

    def verify_user_for_login(self, username, password):
        result = self.connect_and_execute(db_constants.SEARCH_USER_BY_USERNAME_AND_PASSWORD, (username, password),
                                          False)
        if result is not None:
            self.is_logged_in = True

    def get_pockets(self):
        result_set = self.connect_and_execute(db_constants.SELECT_POCKETS, None, True)
        pockets = []
        if result_set is not None:
            for result in result_set:
                pocket = Pocket(pocket_id=result[0], name=result[1], amount=result[2])
                pockets.append(pocket)
            return pockets
        else:
            return None

    def get_pocket_by_name(self, pocket_name):
        result = self.connect_and_execute(db_constants.SELECT_POCKET_BY_NAME, (pocket_name,),False)
        if result is not None:
            return result
        else:
            return None

    def get_expense_type_names(self):

        result = self.connect_and_execute(db_constants.GET_EXPENSE_TYPE_NAMES, None, True)

        if result is not None:
            return result
        else:
            return None

    def get_names_by_event_type(self, event_type):
        type_of_event = str(type(event_type))
        if "expense" in type_of_event:
            return self.connect_and_execute(db_constants.GET_EXPENSE_TYPE_NAMES, None, True)
        elif "income" in type_of_event:
            return self.connect_and_execute(db_constants.GET_INCOME_TYPE_NAMES, None, True)

    def get_resume_data(self, month):

        result = self.connect_and_execute(db_constants.GET_EXPENSE_SUM_BY_TYPE_AND_MONTH, month, True)

        if result is not None:
            if len(result) == 0:
                return [('None',0)]
            return result
        else:
            return None

    def get_payroll_by_month(self, month):

        result = self.connect_and_execute(db_constants.GET_PAYROLL_BY_MONTH, month, False)

        if result is not None:
            if len(result) == 0:
                return 0
            return result
        else:
            return 0

    def get_incomes_by_month(self, month):
        results = self.connect_and_execute(db_constants.GET_INCOME_EVENTS_BY_MONTH, month, True)
        income_events = []
        if results is not None:
            for rs in results:
                event = IncomeEvent(rs[0], rs[1], rs[2], rs[3], rs[5])
                income_events.append(event)
            return income_events
        else:
            return None

    def get_expenses_by_month(self, month):
        result_set = self.connect_and_execute(db_constants.GET_EXPENSE_EVENTS_BY_MONTH, month, True)
        expense_events = []
        if result_set is not None:
            for rs in result_set:
                expense = ExpenseEvent(rs[0], rs[1], rs[2], rs[3], rs[4])
                expense_events.append(expense)
            return expense_events
        else:
            return None

    def get_expense_type_by_id(self, id):
        result = self.connect_and_execute(db_constants.GET_EXPENSE_TYPE_BY_ID, id, False)
        if result is not None:
            return result[0]
        else:
            return None

    def insert_expense_type(self,name,note):
        result = self.connect_and_execute(db_constants.INSERT_EXPENSE_TYPE,(name,note),False)
        if result is not None:
            return result[0]
        else:
            return None

    def insert_income_type(self,name,note):
        result = self.connect_and_execute(db_constants.INSERT_INCOME_TYPE,(name,note),False)
        if result is not None:
            return result[0]
        else:
            return None

    def insert_pocket(self,pocket_name,amount):
        result = self.connect_and_execute(db_constants.INSERT_POCKET,(pocket_name,amount),False)
        if result is not None:
            return result
        else:
            return None

    @staticmethod
    def show_options_popup_message(root, message):
        return PopupOptionsMessage(root, message)

    def pocket_name_in_database(self,pocket_name):
        return self.get_pocket_by_name(pocket_name) is not None

    def delete_pocket(self, pocket_name):
        result = self.connect_and_execute(db_constants.DELETE_POCKET_BY_NAME,(pocket_name,),False)
        if result is not None:
            return result
        else:
            return None
