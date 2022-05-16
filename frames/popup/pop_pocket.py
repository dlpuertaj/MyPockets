from tkinter import Toplevel, Button, Label, Entry


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

    def save_pocket(self, serve, pocket_name, pocket_amount):

        if self.validate_initial_amount(pocket_amount):
            if pocket_name != "":
                if not serve.pocket_name_in_database(pocket_name):
                    serve.insert_pocket(pocket_name, pocket_amount)
                    serve.show_popup_message(self.root, "Success!")
                else:
                    serve.show_popup_message(self.root, "Pocket exists!")
            else:
                serve.show_popup_message(self.root, "Name entered is invalid")
        else:
            serve.show_popup_message(self.root, "Amount entered is invalid")

    @staticmethod
    def validate_initial_amount(amount):
        if len(amount) > 0 and amount.isnumeric():
            return True
        else:
            return False
