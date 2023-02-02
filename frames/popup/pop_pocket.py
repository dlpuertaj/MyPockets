import ttkbootstrap as ttkboot

from tkinter import E, W, END
from services import db_services
from services import gui_services

class PopPocket(ttkboot.Toplevel):
    """ Class that creates the popup for creating, updating or deleting a pocket"""

    def __init__(self, root, is_new_pocket):
        if is_new_pocket:
            ttkboot.Toplevel.__init__(self,title='New Pocket')
        else:
            ttkboot.Toplevel.__init__(self,title='Edit Pocket')
        self.pockets = None
        self.account_pocket = None
        self.clicked_pocket = ttkboot.StringVar()
        self.clicked_pocket_id = None
        self.pocket_amount_entry = ttkboot.Entry(self)
        self.pocket_name_entry = ttkboot.Entry(self)
        self.is_new_pocket = is_new_pocket
        self.root = root
        self.grab_set()
        self.choice = None

    def create_and_show_popup(self, db_connection):

        grid_row = 0
        if not self.is_new_pocket:
            self.title("Edit Pocket")
            self.add_edit_pocket_components(db_connection)
            grid_row = 1
        else:
            self.title("New Pocket")

        pocket_name_label = ttkboot.Label(self, text="Name: ")
        pocket_amount_label = ttkboot.Label(self, text="Initial Amount: ")

        save_button = ttkboot.Button(self, text="Save",
                                     bootstyle='primary',
                                     command=lambda: self.save_pocket(db_connection,
                                                                      self.pocket_name_entry.get(),
                                                                      self.pocket_amount_entry.get()))

        delete_button = ttkboot.Button(self, text="Delete",
                                       bootstyle='danger',
                                       command=lambda: self.delete_pocket(db_connection,
                                                                          self.pocket_name_entry.get(),
                                                                          self.pocket_amount_entry.get()))

        pocket_name_label.grid(column=0, row=grid_row, padx=2,pady=2,sticky=W)
        self.pocket_name_entry.grid(column=1, row=grid_row, sticky=E)

        pocket_amount_label.grid(column=0, row=grid_row + 1, padx=2, pady=2, sticky=W)
        self.pocket_amount_entry.grid(column=1, row=grid_row + 1, sticky=E)

        save_button.grid(column=0, row=grid_row + 2, columnspan=2, padx=2,pady=2, sticky=(E, W))
        delete_button.grid(column=0, row=grid_row + 3, columnspan=2, padx=2, pady=2, sticky=(E, W))

    def add_edit_pocket_components(self, db_connection):
        pocket_options = self.get_pockets(db_connection)
        self.add_select_dropdown(pocket_options, "Pocket: ", 0)
        self.pocket_name_entry.insert(0, str(self.account_pocket.get_name()))
        self.pocket_amount_entry.insert(0, str(self.account_pocket.get_amount()))
        self.pocket_amount_entry.config(state="disabled")

    def update_edit_pocket_components(self, db_connection):
        pockets_options = self.get_pockets(db_connection)
        self.add_select_dropdown(pockets_options, "Pocket: ", 0)

    def save_pocket(self, db_connection, pocket_name, pocket_amount):

        if self.validate_initial_amount(pocket_amount):
            if pocket_name != "":
                if db_services.get_pocket_by_name(db_connection, pocket_name) is None:

                    if self.is_new_pocket:
                        db_services.insert_pocket(db_connection, pocket_name, pocket_amount)
                    else:
                        if self.clicked_pocket_id is None:
                            self.clicked_pocket_id = db_services.get_pocket_by_name(
                                db_connection, self.clicked_pocket.get()).get_name()
                        db_services.update_pocket(db_connection, pocket_name, self.clicked_pocket_id)
                        self.update_edit_pocket_components(db_connection)
                    gui_services.show_popup_message(self.root, "Success!")

                else:
                    gui_services.show_popup_message(self.root, "Pocket exists!")
            else:
                gui_services.show_popup_message(self.root, "Name entered is invalid")
        else:
            db_services.insert_pocket(db_connection, pocket_name, "0")
            gui_services.show_popup_message(self.root, "Created empty pocket named: " + pocket_name)

    def delete_pocket(self, db_connection, pocket_name, pocket_amount):

        if pocket_name != "":
            if db_services.get_pocket_by_name(db_connection, pocket_name) is not None:
                pass
                gui_services.show_popup_message(self.root, "Pocket does not exist!")
            else:
                gui_services.show_choice_popup(self.root,self.choice)

                if self.choice == "Yes":
                    if pocket_amount is not None or pocket_amount != "0":
                        print("Positive amount, transferring to Account")
                        db_services.update_pocket_amount(db_connection, "Account",
                                                         int(pocket_amount) + int(self.account_pocket.get_amount()))
                        db_services.update_pocket_amount(db_connection, pocket_name, "0")
                        db_services.delete_pocket(db_connection, pocket_name)
                    else:
                        db_services.delete_pocket(db_connection, pocket_name)
        else:
            gui_services.show_popup_message(self.root, "Name entered is invalid")

    @staticmethod
    def validate_initial_amount(amount):
        if len(amount) > 0 and amount.isnumeric():
            return True
        else:
            return False

    def add_select_dropdown(self, pocket_options, label, grid_row):

        self.clicked_pocket.set(pocket_options[0])
        self.clicked_pocket.trace("w", self.pocket_selection_callback)

        type_label = ttkboot.Label(self, text=label)
        type_label.grid(column=0, row=grid_row, padx=2,pady=2,sticky=W)
        dropdown = ttkboot.Combobox(self, textvariable=self.clicked_pocket, values=pocket_options)
        dropdown.grid(column=1, row=grid_row, sticky=(E, W))

    def pocket_selection_callback(self, *clicked_item):
        self.pocket_amount_entry.config(state="normal")
        self.pocket_amount_entry.delete(0, END)
        self.pocket_name_entry.delete(0, END)
        self.pocket_name_entry.insert(0, self.clicked_pocket.get())
        pocket = self.get_pocket_from_callback(self.clicked_pocket.get())
        self.pocket_amount_entry.insert(0, pocket.get_amount())
        self.pocket_amount_entry.config(state="disabled")

    def get_pockets(self, db_connection):
        pocket_options = []
        self.pockets = db_services.get_pockets(db_connection)
        for pocket in self.pockets:
            pocket_options.append(pocket.name)
            if pocket.get_name() == "Account":
                self.account_pocket = pocket

        return pocket_options

    def get_pocket_from_callback(self, pocket_name):
        for pocket in self.pockets:
            if pocket_name == pocket.get_name():
                self.clicked_pocket_id = pocket.get_id()
                return pocket

    def get_pocket_from_name(self, pocket_name):
        for pocket in self.pockets:
            if pocket_name == pocket.get_name():
                return pocket
