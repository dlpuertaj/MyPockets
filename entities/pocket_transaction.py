class PocketTransaction:
    def __init__(self, pocket_id, target_pocket_id, amount, transaction_date):
        self.pocket_id = pocket_id
        self.target_pocket_id = target_pocket_id
        self.amount = amount
        self.transaction_date = transaction_date