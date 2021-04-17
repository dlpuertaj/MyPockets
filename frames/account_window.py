from tkinter import Frame, Label, Button, ttk, CENTER
from services import Services as serve

class AccountFrame(Frame):

    def __init__(self,root,account):
        super.__init__(root)
        self.account = account
        self.label_total = Label(self,text="Total")
        self.label_name = Label(self)
        self.button_income = Button(self)
        self.button_expense = Button(self,)
        self.table = ttk.Treeview(self)

    def paint_frame(self):
        self.button_income.config(text="New Income")
        self.button_expense(text="New Expense")
        self.label_name.config(text="Account Name")
        self.label_name.pack()
        self.button_income.pack()
        self.button_expense.pack()
        self.table.pack()
        self.label_total.pack()


    def build_transactions_table(self):
        tree = ttk.Treeview(self.main_frame, column=("c1", "c2", "c3","c4"), show='headings')

        tree.column("#1", anchor=CENTER)
        tree.heading("#1", text="DATE")
        tree.column("#2", anchor=CENTER)
        tree.heading("#2", text="TYPE")
        tree.column("#3", anchor=CENTER)
        tree.heading("#3", text="AMOUNT")
        tree.column("#4", anchor=CENTER)
        tree.heading("#4", text="NOTE")
        tree.pack()

    def get_account_data(self):
        data = serve.get_account_data_by_id(id)
        return data
