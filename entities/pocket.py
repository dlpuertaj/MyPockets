class Pocket:

    def __init__(self, pocket_id, name, amount):
        self.pocket_id = pocket_id
        self.name = name
        self.amount = amount

    def get_name(self):
        return self.name

    def get_id(self):
        return self.pocket_id

    def get_amount(self):
        return self.amount
