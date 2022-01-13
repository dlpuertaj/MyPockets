from datetime import date

class Event:

    def __int__(self):
        today = date.today()
        self.id = None
        self.amount = 0
        self.type = ''
        self.date = today.strftime("%d-%m-%Y")
        self.description = ''

    def __init__(self,event_id,amount,event_type,event_date,description):
        self.id = event_id
        self.amount = amount
        self.type = event_type
        self.date = event_date
        self.description = description

    def show_type(self):
        raise NotImplementedError("Subclass must implement this")

    def has_id(self):
        return self.id is not None