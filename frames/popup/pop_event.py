from tkinter import Toplevel, Button, Label, Entry, OptionMenu, StringVar

import global_constants
from frames.popup.popup_message import PopupGenericMessage

class PopEvent(Toplevel):
    """ Class that creates the popup for a new event"""

    EXPENSE = "Expense"
    INCOME = "Income"
    ACCOUNT = 'Account'
    NEW = "New"
    EDIT = "Edit"

    def __init__(self, root, event_type):
        Toplevel.__init__(self,root)
        self.root = root
        self.event_type = event_type
        self.create_or_update_title = ''
        self.grab_set()
        self.set_create_or_update_title()
        self.title(self.create_or_update_title + " " + self.event_type.show_type())

    def set_create_or_update_title(self):
        if self.event_type.has_id():
            self.create_or_update_title = self.NEW
        else:
            self.create_or_update_title = self.EDIT

    def create_and_show_popup(self,serve):
        types = self.get_type_options_for_dropdown(False) # TODO: Get type from object
        accounts = self.get_type_options_for_dropdown(True)

        type_options = []
        account_options = []
        for t in types:
            type_options.append(t.get_name())

        for account in accounts:
            account_options.append(account.get_name())

        type_label = self.event_type.show_type + " Type"

        clicked_type = StringVar()
        self.add_select_dropdown(type_options, clicked_type, type_label)

        clicked_account = StringVar()
        self.add_select_dropdown(account_options, clicked_account, self.ACCOUNT)

        amount_label = Label(self, text="Amount: ")
        amount_entry = Entry(self)

        date_label = Label(self,text="Date: ")
        date_entry = Entry(self)

        note_label = Label(self,text="Note: ")
        note_entry = Entry(self)

        save_button = Button(self, text="Save", command=lambda: self.save_event(
            serve, types, accounts, clicked_type.get(), amount_entry.get(), date_entry.get(),
            note_entry.get(), clicked_account.get()))

        close_button = Button(self, text="Close", command=self.destroy)

        amount_label.pack()
        amount_entry.pack()
        date_label.pack()
        date_entry.pack()
        note_label.pack()
        note_entry.pack()

        save_button.pack()
        close_button.pack()

    def get_type_options_for_dropdown(self, serve, get_accounts):
        if get_accounts:
            items = serve.get_accounts()
        elif self.event_type:
            items = serve.get_income_types()
        else:
            items = serve.get_expense_types()

        return items

    def add_select_dropdown(self, options, clicked, label):
        clicked.set(options[0])
        type_label = Label(self, text=label)
        type_label.pack()
        dropdown = OptionMenu(self, clicked, *options)
        dropdown.pack()

    def save_event(self, serve, types, accounts, event_type, amount, date, note, account):
        used_account = None
        for t in types:
            if t.get_name() == event_type:
                event_type = t.get_id()
                break

        for a in accounts:
            if a.get_name() == account:
                used_account = a
                account = a.get_id()
                break

        if self.event_type:
            serve.insert_event(True,amount,event_type, date, note, account)
            serve.update_account_amount(used_account.get_id(), (used_account.get_amount() + int(amount)))
            self.show_popup_message(global_constants.SUCCESS_OPERATION)
        else:
            if used_account.get_amount() < int(amount):
                self.show_popup_message(global_constants.AMOUNT_GRATER_THAN_ACCOUNT_AMOUNT)
            else:
                serve.insert_event(False,amount,event_type, date, note, account)
                serve.update_account_amount(used_account.get_id(), (used_account.get_amount() - int(amount)))
                self.show_popup_message(global_constants.SUCCESS_OPERATION)

    def show_popup_message(self,message):
        error_popup = PopupGenericMessage(self.root, message)
        error_popup.grab_set()
        self.wait_window(error_popup)
