from tkinter import Toplevel, Button, Label, Entry, OptionMenu, StringVar
from services import Services as srv

""" Class that creates the popup for a new event"""
class PopEvent(Toplevel):

    LARGE_FONT = ("Verdana", 12)
    NORM_FONT = ("Helvetica", 10)
    SMALL_FONT = ("Helvetica", 8)
    EXPENSE = "Expense"
    INCOME = "Income"
    NEW = "New"
    EDIT = "Edit"

    def __init__(self, root,event_type,event_id):
        Toplevel.__init__(self,root)
        self.root = root
        self.serve = srv()
        self.event_type = event_type
        self.event_id = event_id
        self.expense_or_income = ""
        self.new_or_edit = ""
        self.grab_set()
        self.customize_text()
        self.title(self.new_or_edit + " " + self.expense_or_income)

    def customize_text(self):
        if self.event_type:
            self.expense_or_income = self.INCOME
        else:
            self.expense_or_income = self.EXPENSE

        if self.event_id is None:
            self.new_or_edit = self.NEW
        else:
            self.new_or_edit = self.EDIT

    def create_and_show_popup(self):
        types = self.get_type_options_for_dropdown(False)
        accounts = self.get_type_options_for_dropdown(True)

        type_options = []
        account_options = []
        for t in types:
            type_options.append(t[1])

        for account in accounts:
            account_options.append(account[1])

        type_label = self.expense_or_income + " Type"
        accounts_label = "Account"

        clicked_type = StringVar()
        type_dropdown = self.add_select_dropdown(type_options, clicked_type, type_label)

        clicked_account = StringVar()
        account_dropdown = self.add_select_dropdown(account_options, clicked_account, accounts_label)

        amount_label = Label(self, text="Amount: ")
        amount_entry = Entry(self)

        date_label = Label(self,text="Date: ")
        date_entry = Entry(self)

        note_label = Label(self,text="Note: ")
        note_entry = Entry(self)

        save_button = Button(self, text="Save", command=lambda: self.save_expense_event(
            types, accounts,
            clicked_type.get(), amount_entry.get(), date_entry.get(), note_entry.get(), clicked_account.get()))
        cancel_login_button = Button(self, text="Cancel", command=self.destroy)

        type_dropdown.pack()
        account_dropdown.pack()

        amount_label.pack()
        amount_entry.pack()
        date_label.pack()
        date_entry.pack()
        note_label.pack()
        note_entry.pack()

        save_button.pack()
        cancel_login_button.pack()

    def get_type_options_for_dropdown(self, get_accounts):

        if get_accounts:
            items = self.serve.get_accounts()
        elif self.event_type:  # TODO: Retrieve names only
            items = self.serve.get_income_types()
        else:
            items = self.serve.get_expense_types()

        return items

    def add_select_dropdown(self, options, clicked, label):
        clicked.set(options[0])
        type_label = Label(self, text=label)
        type_label.pack()
        expense_type_menu = OptionMenu(self, clicked, *options)
        return expense_type_menu

    def save_expense_event(self, expense_type, amount, date, note, account):
        self.serve.insert_expense_event(expense_type, amount, date, note, account)
