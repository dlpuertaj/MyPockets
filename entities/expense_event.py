from entities.event import Event


class ExpenseEvent(Event):

    def __init__(self,event_id,expense_amount,expense_type,expense_date,description, required):
        Event.__init__(self,event_id, expense_amount, expense_type, expense_date, description)
        self.required = required

    def get_expense_date(self):
        return self.date

    def get_expense_amount(self):
        return self.amount

    def get_expense_type(self):
        return self.type

    def get_expense_description(self):
        return self.description

    def is_required(self):
        return self.required

    def show_type(self):
        return 'Expense'



