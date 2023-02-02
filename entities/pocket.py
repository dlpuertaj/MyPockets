class Pocket:

    def __init__(self, pocket_id, name, amount):
        self.pocket_id = pocket_id
        self.name = name
        self.amount = amount
        self.transaction_list = []

    def get_name(self):
        return self.name

    def get_id(self):
        return self.pocket_id

    def get_amount(self):
        return self.amount

    def add_transaction(self, transaction):
        self.transaction_list.append(transaction)

    def remove_object(self, transaction):
        self.transaction_list.remove(transaction)

    def get_list(self):
        return self.transaction_list
