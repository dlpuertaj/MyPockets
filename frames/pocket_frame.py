from tkinter import *
from tkinter import ttk

from frames.popup.pop_transfer_to_pocket import PopTransferToPocket
from services import Services as serve


class PocketFrame(Frame):

    """ Initialization method that instantiates the services class and the pocket table"""
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.serve = serve()
        self.pockets_table = ttk.Treeview(self)  # tabla
        self.pockets = None

    """ Method that creates and shows the pocket frame with the database data"""
    def create_pocket_frame(self):
        self.add_transfer_button()
        self.build_pocket_table()
        self.load_pockets_to_table()
        self.pack(side="left", fill=BOTH, expand=1)
        self.pockets_table.pack()

    """ Method that creates the button that creates a new money transfer to a pocket"""
    def add_transfer_button(self):
        add_to_pocket_button = Button(self,
                                      text="Transfer to Pocket",
                                      command=self.transfer_to_pocket)
        add_to_pocket_button.pack()

    """ Method that builds the pocket table with the headers and columns"""
    def build_pocket_table(self):
        self.pockets_table['columns'] = ("Name", "Amount")
        self.pockets_table.heading("0", text="", anchor=W)
        self.pockets_table.column("#0", width=0, stretch=NO)

        self.pockets_table.column("Name", anchor=W, width=100)
        self.pockets_table.column("Amount", anchor=W, width=100)

        self.pockets_table.heading("Name", text="Name", anchor=W)
        self.pockets_table.heading("Amount", text="Amount", anchor=W)

    """ Method that query the data of all the pockets from the database and inserts them in the table"""
    def load_pockets_to_table(self):
        iid = 0
        self.pockets = self.serve.get_pockets()
        for pocket in self.pockets:
            self.pockets_table.insert(parent='', index='end', iid=iid, text="Parent",
                                      values=(pocket.name, pocket.amount))
            iid = iid + 1

    def transfer_to_pocket(self):
        pop_transfer = PopTransferToPocket(self.root, self.pockets)
        pop_transfer.create_and_show_popup(self.serve)
        self.root.wait_window(pop_transfer)
        self.update_pockets_table()

    def update_pockets_table(self):
        self.pockets_table.destroy()
        self.pockets_table = ttk.Treeview(self)
        self.build_pocket_table()
        self.load_pockets_to_table()
        self.pockets_table.pack()


