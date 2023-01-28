from tkinter import Toplevel, Button, Label, Entry, OptionMenu, StringVar, E, W
from services import db_services, gui_services
from entities.pocket_transaction import PocketTransaction

class PopTransferToPocket(Toplevel):
    """ Class that creates the popup for the transfer of amounts between pockets"""

    def __init__(self, root, pockets):
        Toplevel.__init__(self, root)
        self.root = root
        self.grab_set()
        self.pockets = pockets
        self.EXTERNAL_SOURCE = "External Source"

    def create_and_show_popup(self, db_connection):
        pocket_options = [self.EXTERNAL_SOURCE]
        for pocket in self.pockets:
            pocket_options.append(pocket.name)

        clicked_source_pocket = StringVar()
        self.add_select_dropdown(pocket_options, clicked_source_pocket, "From: ",0)

        clicked_target_pocket = StringVar()
        self.add_select_dropdown(pocket_options[1:], clicked_target_pocket, "To: ",1)

        transfer_amount_label = Label(self, text="Amount: ")
        transfer_amount_entry = Entry(self)

        transfer_button = Button(self, text="Transfer",
                                 command=lambda: self.save_transfer(db_connection,
                                                                    clicked_source_pocket.get(),
                                                                    clicked_target_pocket.get(),
                                                                    transfer_amount_entry.get()))

        close_button = Button(self, text="Close", command=self.destroy)

        transfer_amount_label.grid(column=0,row=2,sticky=E)
        transfer_amount_entry.grid(column=1,row=2,sticky=E)

        transfer_button.grid(column=0,row=3,sticky=(E,W))
        close_button.grid(column=1,row=3,sticky=(E,W))

    def add_select_dropdown(self, options, clicked, label,grid_row):
        clicked.set(options[0])
        type_label = Label(self, text=label)
        type_label.grid(column=0,row=grid_row,sticky=(E,W))
        dropdown = OptionMenu(self, clicked, *options)
        dropdown.grid(column=1,row=grid_row,sticky=(E,W))

    # TODO: optimize this code using try-except and much less if conditions
    def save_transfer(self, db_connection, source, target, amount_being_transferred):

        if source == target:
            gui_services.show_popup_message(self.root, "Source pocket and target pocket cannot be the same!")
        elif source != self.EXTERNAL_SOURCE:
            amount_in_source = self.get_amount_from_pocket(source)
            amount_in_target = self.get_amount_from_pocket(target)
            if self.is_amount_valid(amount_in_source, amount_being_transferred):

                new_target_amount = self.calc_new_amount(amount_in_target, int(amount_being_transferred), False)
                new_source_amount = self.calc_new_amount(amount_in_source, int(amount_being_transferred), True)
                db_services.update_pocket_amount(db_connection, source, new_source_amount)
                db_services.update_pocket_amount(db_connection, target, new_target_amount)

                source_pocket = self.get_pocket_by_name(source)
                target_pocket = self.get_pocket_by_name(target)
                transaction = PocketTransaction(source_pocket.get_id(), target_pocket.get_id(),
                                                amount_being_transferred, 'DD-MM-AAAA')
                db_services.insert_transaction(db_connection,transaction)

                gui_services.show_popup_message(self.root,"Success!")
                source_pocket.add_transaction(transaction)
                #self.pockets = db_services.get_pockets(db_connection) # TODO: add transaction to to pocket object
            else:
                gui_services.show_popup_message(self.root, "Make sure the amount entered is valid")
        else:
            amount_in_target = self.get_amount_from_pocket(target)
            new_target_amount = self.calc_new_amount(amount_in_target, int(amount_being_transferred), False)

            source_pocket = self.get_pocket_by_name(source)
            target_pocket = self.get_pocket_by_name(target)
            transaction = PocketTransaction(source_pocket.get_id(), target_pocket.get_id(),
                                            amount_being_transferred, 'DD-MM-AAAA')

            db_services.update_pocket_amount(db_connection, target, new_target_amount)
            source_pocket.add_transaction(transaction)

            source_pocket.add_transaction(transaction)
            #self.pockets = db_services.get_pockets(db_connection) # TODO: add transaction to to pocket object
            gui_services.show_popup_message(self.root,"Success!")

    @staticmethod
    def is_amount_valid(amount_in_source, amount):
        if len(amount) > 0 and amount.isnumeric():
            if amount_in_source >= int(amount):
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def calc_new_amount(original_amount, amount_to_transfer, source_or_target):
        if source_or_target:
            new_amount = original_amount - amount_to_transfer
        else:
            new_amount = original_amount + amount_to_transfer

        return new_amount

    def get_amount_from_pocket(self, pocket):
        return int(self.get_pocket_by_name(pocket).amount)

    def get_pocket_by_name(self, pocket_name): # TODO: Move this to util_services
        for pocket in self.pockets:
            if pocket_name == pocket.name:
                return pocket