import ttkbootstrap as ttkboot
from services import db_services
from services import gui_services

class PopNewType(ttkboot.Toplevel):
    """ Class that creates the popup for creating, updating or deleting a pocket"""

    def __init__(self, root, is_expense_type):
        ttkboot.Toplevel.__init__(self, root)
        self.root = root
        self.resizable(width=False, height=False)
        self.grab_set()
        self.is_expense_type = is_expense_type
        self.type_name = "Expense" if self.is_expense_type else "Income"

    def create_and_show_popup(self,db_connection):
        self.title("New " + str(self.type_name) + " Type")

        type_name_label = ttkboot.Label(self, text="Name: ")
        type_name_entry = ttkboot.Entry(self)
        type_name_label.grid(column=0,row=1,padx=5,pady=5)
        type_name_entry.grid(column=1,row=1,padx=5,pady=5)

        type_note_label = ttkboot.Label(self, text="Note: ")
        type_note_entry = ttkboot.Entry(self)
        type_note_label.grid(column=0,row=2,padx=5,pady=5)
        type_note_entry.grid(column=1,row=2,padx=5,pady=5)

        save_button = ttkboot.Button(self,text="Save", width=10, command=lambda: self.save_type(db_connection,
                                     type_name_entry.get(),
                                     type_note_entry.get()))

        cancel_button = ttkboot.Button(self,text="Close", width=10, bootstyle='danger',command=self.destroy)

        save_button.grid(column=0,row=4,padx=5,pady=5)
        cancel_button.grid(column=1,row=4,padx=5,pady=5)

    def save_type(self,db_connection, name, note):
        if self.is_expense_type:
            db_services.insert_expense_type(db_connection, name,note)
        else:
            db_services.insert_income_type(db_connection, name,note)
        gui_services.show_popup_message(self.root, "Success!")
