import ttkbootstrap as ttkboot
from tkinter import E, W
from services import db_services, gui_services, util_services
from entities.pocket_transaction import PocketTransaction
from datetime import date

class PopTransferToPocket(ttkboot.Toplevel):
    """ Class that creates the popup for the transfer of amounts between pockets"""

    def __init__(self, root, pockets):
        ttkboot.Toplevel.__init__(self, root)
        self.root = root
        self.grab_set()
        self.pockets = pockets
        self.EXTERNAL_SOURCE = "External Source"

    def create_and_show_popup(self, db_connection):
        pocket_options = [self.EXTERNAL_SOURCE]
        for pocket in self.pockets:
            pocket_options.append(pocket.name)

        clicked_source_pocket = ttkboot.StringVar()
        self.add_select_dropdown(pocket_options, clicked_source_pocket, "From: ",0)

        clicked_target_pocket = ttkboot.StringVar()
        self.add_select_dropdown(pocket_options[1:], clicked_target_pocket, "To: ",1)

        transfer_amount_label = ttkboot.Label(self, text="Amount: ")
        transfer_amount_entry = ttkboot.Entry(self)

        transfer_button = ttkboot.Button(self, text="Transfer", width=10,
                                         command=lambda: self.save_transfer_gpt(db_connection,
                                                                                clicked_source_pocket.get(),
                                                                                clicked_target_pocket.get(),
                                                                                transfer_amount_entry.get()))

        close_button = ttkboot.Button(self, text="Close", width=10, command=self.destroy, bootstyle='danger')

        transfer_amount_label.grid(column=0,row=2,padx=5,pady=5)
        transfer_amount_entry.grid(column=1,row=2,padx=5,pady=5)

        transfer_button.grid(column=0,row=3,padx=5,pady=5,sticky=W)
        close_button.grid(column=1,row=3,padx=5,pady=5,sticky=E)

    def add_select_dropdown(self, options, clicked, label,grid_row):
        clicked.set(options[0])
        type_label = ttkboot.Label(self, text=label)
        type_label.grid(column=0,row=grid_row,padx=5,pady=5)
        dropdown = ttkboot.Combobox(self, textvariable=clicked, values=options)
        dropdown.grid(column=1,row=grid_row,padx=5,pady=5)

    def save_transfer_gpt(self, db_connection, source, target, amount_being_transferred):
        today = date.today()
        if source == target:
            gui_services.show_popup_message(self.root, "Source pocket and target pocket cannot be the same!")
        elif source != self.EXTERNAL_SOURCE:
            source_pocket = util_services.get_pocket_by_name(self.pockets, source)
            target_pocket = util_services.get_pocket_by_name(self.pockets, target)
            if util_services.is_amount_valid(source_pocket.get_amount(), amount_being_transferred):
                new_target_amount = util_services.calc_new_amount(target_pocket.get_amount(),
                                                                  int(amount_being_transferred), False)
                new_source_amount = util_services.calc_new_amount(source_pocket.get_amount(),
                                                                  int(amount_being_transferred), True)
                db_services.update_pocket_amount(db_connection, source, new_source_amount)
                db_services.update_pocket_amount(db_connection, target, new_target_amount)

                transaction = PocketTransaction(source_pocket.get_id(), target_pocket.get_id(),
                                                amount_being_transferred, today)
                db_services.insert_transaction(db_connection, transaction)

                gui_services.show_popup_message(self.root, "Success!")
                source_pocket.add_transaction(transaction)
            else:
                gui_services.show_popup_message(self.root, "Make sure the amount entered is valid")
        else:
            target_pocket = util_services.get_pocket_by_name(self.pockets, target)
            new_target_amount = util_services.calc_new_amount(target_pocket.get_amount(), int(amount_being_transferred),
                                                              False)
            db_services.update_pocket_amount(db_connection, target, new_target_amount)

            transaction = PocketTransaction(None, target_pocket.get_id(), amount_being_transferred, today)
            target_pocket.add_transaction(transaction)
            db_services.insert_transaction(db_connection, transaction)
            gui_services.show_popup_message(self.root, "Success!")

    def get_amount_from_pocket(self, pocket_name):
        return int(util_services.get_pocket_by_name(self.pockets, pocket_name).get_amount())
