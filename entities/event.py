from datetime import date

class Event:

    def __int__(self):
        today = date.today()
        self.event_id = None
        self.expense_amount = 0
        self.expense_type = ''
        self.expense_date = today.strftime("%d-%m-%Y")
        self.description = ''

    def __init__(self,event_id,expense_amount,expense_type,expense_date,description):
        self.event_id = event_id
        self.expense_amount = expense_amount
        self.expense_type = expense_type
        self.expense_date = expense_date
        self.description = description

    def show_type(self):
        raise NotImplementedError("Subclass must implement this")

    def has_id(self):
        return self.event_id is not None