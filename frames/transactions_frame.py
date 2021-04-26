from tkinter import Frame, W, NO, BOTH
from tkinter import ttk

from services import Services as serve

class TransactionsFrame(Frame):

    def __init__(self,root_notebook):
        Frame.__init__(self,root_notebook)
        self.serve = serve()
        self.transactions_table = ttk.Treeview(self)

    def create_transaction_frame(self,month):
        self.build_transactions_table()
        self.data_to_transactions_table_by_month(month)
        self.pack()

    def build_transactions_table(self):
        columns = []

        expense_types = self.serve.get_expense_types()
        for expense_type in expense_types:
            columns.append(expense_type[0])

        self.transactions_table['columns'] = columns
        self.transactions_table.heading("0", text="", anchor=W)
        self.transactions_table.column("#0", width=0, stretch=NO)

        self.transactions_table.column("Income", anchor=W, width=100)
        self.transactions_table.column("Note", anchor=W, width=100)
        self.transactions_table.column("Day", anchor=W, width=100)
        self.transactions_table.heading("Income", text="Income", anchor=W)
        self.transactions_table.heading("Note", text="Note", anchor=W)
        self.transactions_table.heading("Day", text="Day", anchor=W)
        for column in columns:
            self.transactions_table.column(column, anchor=W, width=100)

        for column in columns:
            self.transactions_table.heading(column, text=column, anchor=W)

    def data_to_transactions_table_by_month(self, month):
        incomes_by_month = self.serve.get_incomes_by_month(month)
        expenses_by_month = self.serve.get_expenses_by_month(month)
        data_for_table = []
        days = 30
  #      for day in range(1,days+1):
   #         transaction = ()


"""
            self.resume_table.insert(parent='', index='end', iid=0,
                                     text="Parent", values=amount_for_table)

            self.resume_table.insert(parent='', index='end', iid=1, text="Parent", values=percent_for_table)
            self.transactions_table.column(income, anchor=W, width=100)

        for income in incomes_by_month:
            self.transactions_table.heading(, text=column, anchor=W)
"""


