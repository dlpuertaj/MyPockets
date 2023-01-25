from tkinter import *
from tkinter import ttk

from frames.popup.pop_transfer_to_pocket import PopTransferToPocket
from services import data_services, gui_services


class PocketFrame(ttkboot.Frame):

    """ Initialization method that instantiates the services class and the pocket table"""
    def __init__(self, root,pockets):
        Frame.__init__(self, root)
        self.root = root
        self.pockets_table = ttk.Treeview(self)  # tabla
        self.pockets = pockets

    """ Method that creates and shows the pocket frame with the database data"""
    def create_pocket_frame(self, db_connection):
        self.add_transfer_button(db_connection)
        self.build_pocket_table()
        self.load_pockets_to_table()
        self.pack(side="left", fill=BOTH, expand=1)
        self.pockets_table.pack()

    """ Method that creates the button that creates a new money transfer to a pocket"""
    def add_transfer_button(self, db_connection):
        add_to_pocket_button = Button(self,
                                      text="Transfer to Pocket",
                                      command=lambda: self.transfer_to_pocket(db_connection))
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
        for pocket in self.pockets:
            self.pockets_table.insert(parent='', index='end', iid=iid, text="Parent",
                                      values=(pocket.name, pocket.amount))
            iid = iid + 1

    def transfer_to_pocket(self,db_connection):

        if len(self.pockets) == 0:
            gui_services.show_popup_message(self.root, "No pockets created")
        else:
            pop_transfer = PopTransferToPocket(self.root, self.pockets)
            pop_transfer.create_and_show_popup(db_connection)
            self.root.wait_window(pop_transfer)
            self.update_pockets_table(db_connection)

    def update_pockets_table(self, db_connection):
        self.set_pockets(data_services.get_pockets(db_connection))
        self.pockets_table.destroy()
        self.pockets_table = ttkboot.Treeview(self)
        self.build_pocket_table()
        self.load_pockets_to_table()
        self.pockets_table.pack()

    def set_pockets(self,pockets):
        self.pockets = pockets
