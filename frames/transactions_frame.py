from tkinter import Frame, W, NO, BOTH, Button
from tkinter import ttk

from services import Services as serve


class TransactionsFrame(Frame):

    def __init__(self, root_notebook):
        Frame.__init__(self, root_notebook)
        self.serve = serve()
        self.expense_columns = {}
        self.transactions_table = ttk.Treeview(self)

    def create_transaction_frame(self, month):
        self.build_transactions_table()
        self.data_to_transactions_table_by_month(month)
        self.pack(side="right", fill=BOTH, expand=1)
        self.transactions_table.pack()
        self.create_and_pack_buttons()

    def build_transactions_table(self):
        columns = []
        columns.append("Income")
        columns.append("Note")
        columns.append("Day")
        expense_types = self.serve.get_expense_type_names()
        index = 3
        for expense_type in expense_types:
            self.expense_columns[expense_type[0]] = index
            columns.append(expense_type[0])
            index += 1

        self.transactions_table['columns'] = columns
        self.transactions_table.heading("0", text="", anchor=W)
        self.transactions_table.column("#0", width=0, stretch=NO)

        for column in columns:
            self.transactions_table.column(column, anchor=W, width=100)

        for column in columns:
            self.transactions_table.heading(column, text=column, anchor=W)

    def data_to_transactions_table_by_month(self, month):
        incomes_by_month = self.serve.get_incomes_by_month((month,))
        expenses_by_month = self.serve.get_expenses_by_month((month,))
        expense_type_names = self.serve.get_expense_type_names()
        days = 30

        iid = 0

        for day in range(1, days+1):
            data_for_table = [0, '', day]
            for expense in expense_type_names:
                data_for_table.append(0)
            self.transactions_table.insert(parent='', index='end', iid=iid,
                                           text="Parent", values=data_for_table)
            iid = iid + 1

        self.add_income_to_table(incomes_by_month)
        self.add_expenses_to_table(expenses_by_month)

    def add_income_to_table(self,incomes_by_month):
        for income in incomes_by_month:
            for row in range(len(self.transactions_table.get_children())):
                row_values = self.transactions_table.item(row)['values']
                if self.get_day_from_date(income.income_date) == str(row_values[2]):
                    row_with_new_income = row_values
                    row_with_new_income[0] += income.income_amount
                    self.transactions_table.item(row, text="", values=row_with_new_income)

    def add_expenses_to_table(self,expenses_by_month):
        for expense in expenses_by_month:
            for row in range(len(self.transactions_table.get_children())):
                row_values = self.transactions_table.item(row)['values']
                if self.get_day_from_date(expense[2]) == str(row_values[2]):
                    row_with_new_expense = row_values
                    index = self.expense_columns[expense[0]]

                    row_with_new_expense[index] += expense[1]

                    self.transactions_table.item(row, text="", values=row_with_new_expense)

    def create_and_pack_buttons(self):
        new_income_button = Button(self, text="New Income", command="")
        new_expense_button = Button(self, text="New Expense", command="")
        new_income_button.pack()
        new_expense_button.pack()

    @staticmethod
    def get_day_from_date(date):
        return date.split('-')[2]

    def build_data_for_table(self, incomes, expenses):
        return []


"""
            self.resume_table.insert(parent='', index='end', iid=0,
                                     text="Parent", values=amount_for_table)

            self.resume_table.insert(parent='', index='end', iid=1, text="Parent", values=percent_for_table)
            self.transactions_table.column(income, anchor=W, width=100)

        for income in incomes_by_month:
            self.transactions_table.heading(, text=column, anchor=W)
"""
