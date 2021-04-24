from tkinter import Frame, Button, BOTH, ttk,W,NO
from services import Services as serve

class PocketFrame(Frame):

    def __init__(self,root):
        super.__init__(root)
        self.serve = serve()
        self.pockets_table = ttk.Treeview(self)

    def build_pocket_frame(self):
        self.customize_pocket_frame()
        self.build_pocket_table()
        self.load_pockets_to_table()
        self.pack(side="left", fill=BOTH, expand=1)
        self.pockets_table.pack()

    def customize_pocket_frame(self):
        new_income_button = Button(self, text="New Income",command="")
        new_expense_button = Button(self, text="New Expense",command="")
        new_income_button.pack()
        new_expense_button.pack()

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