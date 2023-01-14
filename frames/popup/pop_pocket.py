from tkinter import Toplevel, Button, Label, Entry, E, W, OptionMenu, StringVar, END


class PopPocket(Toplevel):
    """ Class that creates the popup for creating, updating or deleting a pocket"""

    def __init__(self, root, new_pocket):
        Toplevel.__init__(self, root)
        self.pockets = None
        self.clicked_pocket = StringVar()
        self.clicked_pocket_id = None
        self.pocket_amount_entry = Entry(self)
        self.pocket_name_entry = Entry(self)
        self.new_pocket = new_pocket
        self.root = root
        self.grab_set()
        self.choice = None

    def create_and_show_popup(self, serve):

        grid_row = 0
        if not self.new_pocket:
            self.add_edit_pocket_components(serve)
            grid_row = 1

        pocket_name_label = Label(self, text="Name: ")
        pocket_amount_label = Label(self, text="Initial Amount: ")

        save_button = Button(self, text="Save", command=lambda: self.save_pocket(serve,
                                                                                 self.pocket_name_entry.get(),
                                                                                 self.pocket_amount_entry.get()))

        delete_button = Button(self, text="Delete", command=lambda: self.delete_pocket(serve,
                                                                                       self.pocket_name_entry.get(),
                                                                                       self.pocket_amount_entry.get()))

        # close_button = Button(self, text="Close", command=self.destroy)

        pocket_name_label.grid(column=0, row=grid_row, sticky=E)
        self.pocket_name_entry.grid(column=1, row=grid_row, sticky=E)

        pocket_amount_label.grid(column=0, row=grid_row + 1, sticky=E)
        self.pocket_amount_entry.grid(column=1, row=grid_row + 1, sticky=E)

        save_button.grid(column=0, row=grid_row + 2, sticky=(E, W))
        delete_button.grid(column=1, row=grid_row + 2, sticky=(E, W))
        # close_button.grid(column=2, row=grid_row + 2, sticky=(E, W))

    def add_edit_pocket_components(self, serve):
        pocket_options = self.get_pockets(serve)
        self.add_select_dropdown(pocket_options, "Pocket: ", 0)
        self.pocket_name_entry.insert(0, str(self.pockets[0].get_name()))
        self.pocket_amount_entry.insert(0, str(self.pockets[0].get_amount()))
        self.pocket_amount_entry.config(state="disabled")

    def update_edit_pocket_components(self, serve):
        pockets_options = self.get_pockets(serve)
        self.add_select_dropdown(pockets_options, "Pocket: ", 0)

    def save_pocket(self, serve, pocket_name, pocket_amount):

        if self.validate_initial_amount(pocket_amount):
            if pocket_name != "":
                if not serve.pocket_name_in_database(pocket_name):

                    if self.new_pocket:
                        serve.insert_pocket(pocket_name, pocket_amount)
                    else:
                        if self.clicked_pocket_id is None:
                            self.clicked_pocket_id = self.get_pocket_from_name(self.clicked_pocket.get()).get_id()
                        serve.update_pocket(pocket_name, self.clicked_pocket_id)
                        self.update_edit_pocket_components(serve)
                    serve.show_popup_message(self.root, "Success!")

                else:
                    serve.show_popup_message(self.root, "Pocket exists!")
            else:
                serve.show_popup_message(self.root, "Name entered is invalid")
        else:
            serve.insert_pocket(pocket_name, "0")
            serve.show_popup_message(self.root, "Created empty pocket named: " + pocket_name)

    def delete_pocket(self, serve, pocket_name, pocket_amount):

        if pocket_name != "":
            if not serve.pocket_name_in_database(pocket_name):
                pass
                serve.show_popup_message(self.root, "Pocket does not exist!")
            else:
                popup = serve.show_options_popup_message(self.root, "Pockets amount will be deleted. "
                                                                    "Are you sure?")

                self.handle_popup(popup)
                self.choice = popup.get_choice()

                response = self.choice

                if response == "Yes":
                    print("Yes")
                else:
                    print("No")
        else:
            serve.show_popup_message(self.root, "Name entered is invalid")

    def handle_popup(self,popup):
        popup.grab_set()
        self.root.wait_window(popup)

    @staticmethod
    def validate_initial_amount(amount):
        if len(amount) > 0 and amount.isnumeric():
            return True
        else:
            return False

    def add_select_dropdown(self, pocket_options, label, grid_row):

        self.clicked_pocket.set(pocket_options[0])
        self.clicked_pocket.trace("w", self.pocket_selection_callback)

        type_label = Label(self, text=label)
        type_label.grid(column=0, row=grid_row, sticky=(E, W))
        dropdown = OptionMenu(self, self.clicked_pocket, *pocket_options)
        dropdown.grid(column=1, row=grid_row, sticky=(E, W))

    def pocket_selection_callback(self, *clicked_item):
        self.pocket_name_entry.delete(0, END)
        self.pocket_name_entry.insert(0, self.clicked_pocket.get())
        pocket = self.get_pocket_from_callback(self.clicked_pocket.get())
        self.pocket_amount_entry.insert(0, pocket.get_amount())

    def get_pockets(self, serve):
        pocket_options = []
        self.pockets = serve.get_pockets()
        for pocket in self.pockets:
            pocket_options.append(pocket.name)

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
