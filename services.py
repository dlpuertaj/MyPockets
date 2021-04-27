from database.database_manager import DatabaseManager as db
from database import database_constants as db_constants
from sqlite3 import Error as error_sqlite


class Services:

    def __init__(self):
        self.db_manager = db()
        self.is_logged_in = False

    def connect_and_execute(self,query,data,multi):
        connection = None
        try:
            connection = self.db_manager.create_connection(True)
            result = self.db_manager.execute_sqlite_query(connection,
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
        result = self.connect_and_execute(db_constants.SEARCH_USER_BY_USERNAME_AND_PASSWORD,(username, password),False)
        if result is not None:
            self.is_logged_in = True

    def get_account_data_by_id(self, id):
        result = self.connect_and_execute(db_constants.GET_ACCOUNT_DATA_BY_ID,id,False)

        if result is not None:
            return result
        else:
            return None

    def get_pockets(self):
        result = self.connect_and_execute(db_constants.SELECT_POCKETS,None,True)

        if result is not None:
            return result
        else:
            return None

    def get_expense_types(self):

        result = self.connect_and_execute(db_constants.GET_EXPENSE_TYPES,None,True)

        if result is not None:
            return result
        else:
            return None

    def get_resume_data(self,month):

        result = self.connect_and_execute(db_constants.GET_EXPENSE_SUM_BY_TYPE_AND_MONTH,month,True)

        if result is not None:
            return result
        else:
            return None

    def get_payroll_by_month(self,month):

        result = self.connect_and_execute(db_constants.GET_PAYROLL_BY_MONTH,month,False)

        if result is not None:
            return result
        else:
            return None

    def get_incomes_by_month(self, month):
        result = self.connect_and_execute(db_constants.GET_INCOME_EVENTS_BY_MONTH,month,True)
        if result is not None:
            return result
        else:
            return None

    def get_expenses_by_month(self, month):
        result = self.connect_and_execute(db_constants.GET_EXPENSE_EVENTS_BY_MONTH,month,True)
        if result is not None:
            return result
        else:
            return None
