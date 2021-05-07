class Account:

    def __init__(self, account_id, name, amount):
        self.__account_id = account_id
        self.__name = name
        self.__amount = amount

    def get_id(self):
        return self.__account_id

    def get_name(self):
        return self.__name

    def get_amount(self):
        return self.__amount