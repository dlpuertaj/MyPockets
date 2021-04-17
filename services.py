from database_manager import DatabaseManager as db
import database_constants as db_constants
from sqlite3 import Error as error_sqlite

class Services:

    def __init__(self):
        self.db_manager = db()
        self.is_logged_in = False


    def verify_user_for_login(self, username, password):
        connection = None
        try:
            connection = self.db_manager.create_connection(True)
            result = self.db_manager.execute_sqlite_query(connection,
                                                          db_constants.SEARCH_USER_BY_USERNAME_AND_PASSWORD,
                                                          (username,password),
                                                          False)
        except error_sqlite as e:
            print(e)
        finally:
            if connection is not None:
                connection.close()

        if result is not None:
            self.is_logged_in = True

    @classmethod
    def get_account_data_by_id(self, id):
        connection = None
        try:
            connection = self.db_manager.create_connection(True)
            result = self.db_manager.execute_sqlite_query(connection,
                                                          db_constants.GET_ACCOUNT_DATA_BY_ID,
                                                          id,
                                                          False)
        except error_sqlite as e:
            print(e)
        finally:
            if connection is not None:
                connection.close()

        if result is not None:
            return result
        else:
            return None

