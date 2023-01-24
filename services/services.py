from database import database_constants as db_constants

from entities.expense_event import ExpenseEvent
from entities.income_event import IncomeEvent
from frames.popup.popup_options_message import PopupOptionsMessage

class Services:

    def __init__(self):
        self.is_logged_in = False

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

    @staticmethod
    def show_options_popup_message(root, message):
        return PopupOptionsMessage(root, message)
