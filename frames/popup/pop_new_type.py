from tkinter import Toplevel, Button, Label, Entry, OptionMenu, StringVar, E, W
from services import db_services
from services import gui_services

class PopNewType(Toplevel):
    """ Class that creates the popup for creating, updating or deleting a pocket"""

    def __init__(self, root, expense_or_income):
        Toplevel.__init__(self, root)
        self.root = root
        self.resizable(width=False, height=False)
        self.grab_set()
        self.expense_or_income = expense_or_income
        self.type_name = "Expense" if self.expense_or_income else "Income"

    def create_and_show_popup(self,db_connection):

        type_name_label = Label(self, text="Name: ")
        type_name_entry = Entry(self)

        type_note_label = Label(self, text="Note: ")
        type_note_entry = Entry(self)

        save_button = Button(self,text="Save",
                             command=lambda: self.save_type(db_connection,
                                                            type_name_entry.get(),
                                                            type_note_entry.get()))

        cancel_button = Button(self,text="Close", command=self.destroy)

        title_label = Label(self, text="==== New " + str(self.type_name) + " Type ====")
        title_label.grid(column=0,row=0,columnspan=2)
        type_name_label.grid(column=0,row=1,sticky=W)
        type_name_entry.grid(column=1,row=1)

        type_note_label.grid(column=0,row=2,sticky=W)
        type_note_entry.grid(column=1,row=2)

        save_button.grid(column=0,row=3,pady=7,sticky=(E, W))
        cancel_button.grid(column=1,row=3,pady=7,sticky=(E, W))

    def save_type(self,db_connection, name, note):
        if self.expense_or_income:
            data_services.insert_expense_type(db_connection, name,note)
        else:
            data_services.insert_income_type(db_connection, name,note)
        gui_services.show_popup_message(self.root, "Success!")
