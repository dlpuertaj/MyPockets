from tkinter import Toplevel, Button, Label, Entry, OptionMenu, StringVar
from services import Services as srv
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
        if self.event_type: # TODO: Retrieve names only
            types = self.serve.get_income_types()
        else:
            types = self.serve.get_expense_types()
        options = []

        for t in types:
            options.append(t[1])

        clicked = StringVar()
        clicked.set(options)

        type_label = Label(self,text=(self.expense_or_income + " Type"))
        type_label.pack()
        expense_type_menu = OptionMenu(self,clicked,*options)
        expense_type_menu.pack()
        # TODO: create account option menu

        amount_label = Label(self, text="Amount: ")
        amount_entry = Entry(self)

        date_label = Label(self,text="Date: ")
        date_entry = Entry(self)

        note_label = Label(self,text="Note: ")
        note_entry = Entry(self)

        save_button = Button(self, text="Cancel", command=self.save_expense_event)
        cancel_login_button = Button(self, text="Save", command=self.destroy)

        amount_label.pack()
        amount_entry.pack()
        date_label.pack()
        date_entry.pack()
        note_label.pack()
        note_entry.pack()

        save_button.pack()
        cancel_login_button.pack()

    def save_expense_event(self):
       return None
