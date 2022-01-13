from entities.event import Event


class IncomeEvent(Event):

    def __init__(self, event_id, income_amount, income_type, income_date,description):
        Event.__init__(self,event_id, income_amount, income_type, income_date, description)

    def get_income_date(self):
        return self.date

    def get_income_amount(self):
        return self.amount

    def get_income_type(self):
        return self.type

    def get_income_description(self):
        return self.description

    def show_type(self):
        return 'Income'
