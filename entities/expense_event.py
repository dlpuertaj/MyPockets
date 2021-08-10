class ExpenseEvent:
    def __init__(self,event_id,expense_amount,expense_type,expense_date,
                 description):
        self.event_id = event_id
        self.expense_amount = expense_amount
        self.expense_type = expense_type
        self.expense_date = expense_date
        self.description = description
