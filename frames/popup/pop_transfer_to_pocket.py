from tkinter import Toplevel, Button, Label, Entry, OptionMenu, StringVar
from datetime import date
import global_constants
from frames.popup.popup_message import PopupGenericMessage


class PopTransferToPocket(Toplevel):
    """ Class that creates the popup for creating, updating or deleting a pocket"""


    def __init__(self, root, pockets):
        Toplevel.__init__(self, root)
        self.root = root
        self.grab_set()
        self.pockets = pockets
        self.EXTERNAL_SOURCE = "External Source"

    def create_and_show_popup(self, serve):
        pocket_options = [self.EXTERNAL_SOURCE]
        for pocket in self.pockets:
            pocket_options.append(pocket.name)

        clicked_source_pocket = StringVar()
        self.add_select_dropdown(pocket_options, clicked_source_pocket, "From: ")

        clicked_target_pocket = StringVar()
        self.add_select_dropdown(pocket_options[1:], clicked_target_pocket, "To: ")

        transfer_amount_label = Label(self, text="Amount: ")
        transfer_amount_entry = Entry(self)

        transfer_button = Button(self, text="Transfer", command=lambda: self.save_pocket(
            serve,
            clicked_source_pocket.get(),
            clicked_target_pocket.get(),
            transfer_amount_entry.get()))

        close_button = Button(self, text="Close", command=self.destroy)

        transfer_amount_label.pack()
        transfer_amount_entry.pack()

        transfer_button.pack()
        close_button.pack()

    def add_select_dropdown(self, options, clicked, label):
        clicked.set(options[0])
        type_label = Label(self, text=label)
        type_label.pack()
        dropdown = OptionMenu(self, clicked, *options)
        dropdown.pack()

    # TODO: optimize this code using try-except and much less if conditions
    def save_transfer(self, serve, source, target, amount):
        new_source_amount = self.set_new_amount(True)
        new_target_amount = self.set_new_amount(False)
        serve.update_pocket_amount(source,new_source_amount)
        serve.update_pocket_amount(target,new_target_amount)

    def set_new_amount(self, param):
        pass
