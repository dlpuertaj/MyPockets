from entities.event import Event


class ExpenseEvent(Event):

    def __int__(self):
        Event.__init__(self)

    def __init__(self,event_id,expense_amount,expense_type,expense_date,description):
        Event.__init__(self,event_id, expense_amount, expense_type, expense_date, description)

    def show_type(self):
        return 'Expense'



