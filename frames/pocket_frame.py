from tkinter import *
from tkinter import ttk

from services import Services as serve

class PocketFrame(Frame):

    def __init__(self,root):
        Frame.__init__(self,root)
        self.serve = serve()
        self.pockets_table = ttk.Treeview(self)

    def create_pocket_frame(self):
        self.build_pocket_table()
        self.load_pockets_to_table()
        self.pack(side="left", fill=BOTH, expand=1)
        self.pockets_table.pack()
        self.add_transfer_button()

    def add_transfer_button(self):
        add_to_pocket_button = Button(self, text="Transfer to Pocket",command="")
        add_to_pocket_button.pack()

    def build_pocket_table(self):
        self.pockets_table['columns'] = ("Name", "Amount")
        self.pockets_table.heading("0", text="", anchor=W)
        self.pockets_table.column("#0", width=0, stretch=NO)

        self.pockets_table.column("Name", anchor=W, width=100)
        self.pockets_table.column("Amount", anchor=W, width=100)

        self.pockets_table.heading("Name", text="Name", anchor=W)
        self.pockets_table.heading("Amount", text="Amount", anchor=W)

    def load_pockets_to_table(self):
        iid = 0
        pockets_data = self.serve.get_pockets()
        for pocket in pockets_data:
            self.pockets_table.insert(parent='', index='end', iid=iid, text="Parent", values=(pocket[1], pocket[2]))
            iid = iid + 1