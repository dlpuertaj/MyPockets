from tkinter import Toplevel, Button, Label, Entry, OptionMenu, StringVar
from services import Services as srv
class PopExpense(Toplevel):
    LARGE_FONT = ("Verdana", 12)
    NORM_FONT = ("Helvetica", 10)
    SMALL_FONT = ("Helvetica", 8)

    def __init__(self, root,expense_id):
        Toplevel.__init__(self,root)
        self.root = root
        self.serve = srv()
        self.expense_id = expense_id
        self.grab_set()
        self.title("Expense")
        self.save_button = Button(self)
        self.expense_type_label = Label(self)
        self.expense_type_menu = None
        self.expense_amount_entry = Entry(self)

    def create_and_show_popup(self):
        expense_types = self.serve.get_expense_types()
        options = []
        for type in expense_types:
            options.append(type[1])
        clicked = StringVar()
        clicked.set(options)
        self.expense_type_menu = OptionMenu(self,clicked,*options)
        self.expense_type_menu.pack()
        cancel_login_button = Button(self, text="Cancel", command=self.destroy)
        cancel_login_button.pack()
