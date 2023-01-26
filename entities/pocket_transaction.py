class PocketTransaction:
    def __init__(self, pocket_id, source_pocket_id, income_type_id, expense_type_id, amount, date):
        self.pocket_id = pocket_id
        self.source_pocket_id = source_pocket_id
        self.income_type_id = income_type_id
        self.expense_type_id = expense_type_id
        self.amount = amount
        self.date = date