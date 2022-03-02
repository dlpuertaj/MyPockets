from tkinter import Toplevel, Button, Label, Entry, OptionMenu, StringVar
from datetime import date
import global_constants
from frames.popup.popup_message import PopupGenericMessage


class PopPocket(Toplevel):
    """ Class that creates the popup for creating, updating or deleting a pocket"""

    def __init__(self, root):
        Toplevel.__init__(self, root)
        self.root = root
        self.grab_set()

    def create_and_show_popup(self, serve):

        pocket_name_label = Label(self, text="Name: ")
        pocket_name_entry = Entry(self)

        pocket_amount_label = Label(self, text="Initial Amount: ")
        pocket_amount_entry = Entry(self)

        save_button = Button(self, text="Save", command=lambda: self.save_pocket(
            serve, pocket_name_entry.get(), pocket_amount_entry.get()))

        close_button = Button(self, text="Close", command=self.destroy)

        pocket_name_label.pack()
        pocket_name_entry.pack()

        pocket_amount_label.pack()
        pocket_amount_entry.pack()

        save_button.pack()
        close_button.pack()

    # TODO: optimize this code using try-except and much less if conditions
    def save_pocket(self, serve, pocket_name, pocket_amount):
        if len(pocket_amount) > 0:
            if pocket_amount.isnumeric():
                if int(pocket_amount) < 0:
                    serve.show_popup_message(self.root, "Amount entered is invalid")
                elif pocket_name is not "":
                    if not self.pocket_in_database(pocket_name):
                        serve.insert_pocket(pocket_name, pocket_amount)
                    else:
                        serve.show_popup_message(self.root, "Pocket exists!")
            else:
                serve.show_popup_message(self.root, "Amount entered is invalid")
        elif pocket_amount == "":
            if pocket_name is not "":
                if not self.pocket_in_database(serve, pocket_name):
                    serve.insert_pocket(pocket_name, 0)
                else:
                    serve.show_popup_message(self.root, "Pocket exists!")
            else:
                serve.show_popup_message(self.root, "Name entered is invalid")

    def pocket_in_database(self, serve,pocket_name):
        return serve.get_pocket_by_name(pocket_name) is not None