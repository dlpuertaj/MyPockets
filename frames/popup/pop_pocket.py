from tkinter import Toplevel, Button, Label, Entry, E, W, OptionMenu, StringVar


class PopPocket(Toplevel):
    """ Class that creates the popup for creating, updating or deleting a pocket"""

    def __init__(self, root, new_or_edit):
        Toplevel.__init__(self, root)
        self.clicked_pocket = StringVar()
        self.pocket_amount_entry = Entry(self)
        self.pocket_name_entry = Entry(self)
        self.new_or_edit = new_or_edit
        self.root = root
        self.grab_set()

    def create_and_show_popup(self, serve):

        if not self.new_or_edit:
            pocket_options = []
            pockets = serve.get_pockets()
            for pocket in pockets:
                pocket_options.append(pocket.name)

            self.add_select_dropdown(pocket_options, "Pocket: ", 0)
            self.pocket_amount_entry.config()
        pocket_name_label = Label(self, text="Name: ")
        self.pocket_name_entry = Entry(self)

        pocket_amount_label = Label(self, text="Initial Amount: ")
        self.pocket_amount_entry = Entry(self)

        save_button = Button(self, text="Save", command=lambda: self.save_pocket(
            serve, self.pocket_name_entry.get(), self.pocket_amount_entry.get()))

        close_button = Button(self, text="Close", command=self.destroy)

        grid_row = 0
        if not self.new_or_edit:
            grid_row = 1
        pocket_name_label.grid(column=0,row=grid_row,sticky=E)
        self.pocket_name_entry.grid(column=1, row=grid_row,sticky=E)

        pocket_amount_label.grid(column=0, row=grid_row + 1,sticky=E)
        self.pocket_amount_entry.grid(column=1, row=grid_row + 1,sticky=E)

        save_button.grid(column=0, row=grid_row + 2,sticky=(E,W))
        close_button.grid(column=1, row=grid_row + 2,sticky=(E,W))

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
            serve.show_popup_message(self.root, "Amount entered is invalid or empty")

    @staticmethod
    def validate_initial_amount(amount):
        if len(amount) > 0 and amount.isnumeric():
            return True
        else:
            return False

    def add_select_dropdown(self, options, label,grid_row):
        self.clicked_pocket.set(options[0])
        self.clicked_pocket.trace("w", self.pocket_selection_callback)
        type_label = Label(self, text=label)
        type_label.grid(column=0,row=grid_row,sticky=(E,W))
        dropdown = OptionMenu(self, self.clicked_pocket, *options)
        dropdown.grid(column=1,row=grid_row,sticky=(E,W))

    def pocket_selection_callback(self,*clicked_item):

        self.pocket_name_entry.insert(0,self.clicked_pocket.get())
        self.pocket_amount_entry.insert(0,"")