from tkinter import Frame, W, NO, BOTH, Button, StringVar, Label, OptionMenu, Scrollbar
from tkinter import ttk

from services import Services as serve

import calendar as calendar

class TransactionsFrame(Frame):

    months = {}

    """ Initializer method for the transactions frame"""
    def __init__(self, root_notebook,expense_types):
        Frame.__init__(self, root_notebook)
        self.set_months()
        self.clicked_month = StringVar()
        self.serve = serve()
        self.expense_columns = {}
        self.expense_types = expense_types # self.serve.get_expense_types()
        self.transactions_table = ttk.Treeview(self,height=31)

    def set_months(self):
        self.months = {month: str(index) for index, month in enumerate(calendar.month_name) if month}
        for month in self.months:
            if len(self.months[month]) == 1:
                self.months[month] = '0'+self.months[month]

    """ Method that creates de transactions frame"""
    def create_transaction_frame(self, month):
        self.create_select_month_option_menu()
        self.build_transactions_table()
        self.data_to_transactions_table_by_month(month)
        self.pack(side="right", fill=BOTH, expand=1)
        self.transactions_table.pack()
        # self.create_and_pack_buttons()

    def create_select_month_option_menu(self):
        # months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        self.clicked_month.set('January')
        self.clicked_month.trace("w", self.callback)
        type_label = Label(self, text="Month")
        type_label.pack()
        dropdown = OptionMenu(self, self.clicked_month, *self.months.keys())
        dropdown.pack()

    """ Method that builds the transactions table with de database data"""
    def build_transactions_table(self):
        columns = ["Income", "Note", "Day"]
        #expense_types = self.serve.get_expense_type_names()
        index = 3
        for expense_type in self.expense_types:
            self.expense_columns[expense_type.get_name()] = index
            columns.append(expense_type.get_name())
            index += 1

        columns.append("Pocket")

        self.transactions_table['columns'] = columns
        self.transactions_table.heading("0", text="", anchor=W)
        self.transactions_table.column("#0", width=20, stretch=NO)

        for column in columns:
            self.transactions_table.column(column, anchor=W, width=50)

        for column in columns:
            self.transactions_table.heading(column, text=column, anchor=W)

    """ Method that adds the database data to the table"""
    def data_to_transactions_table_by_month(self, month):
        incomes_by_month = self.serve.get_incomes_by_month((month,))
        expenses_by_month = self.serve.get_expenses_by_month((month,))
        expense_type_names = self.get_expense_type_names()
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

    """ Method that adds the income data to the transactions table"""
    def add_income_to_table(self,incomes_by_month):
        for income in incomes_by_month:
            for row in range(len(self.transactions_table.get_children())):
                row_values = self.transactions_table.item(row)['values']
                if self.get_day_from_date(income.get_income_date()) == str(row_values[2]):
                    row_with_new_income = row_values
                    row_with_new_income[0] += income.get_income_amount()
                    self.transactions_table.item(row, text="", values=row_with_new_income)

    """ Method that adds the expense data to the transactions table"""
    def add_expenses_to_table(self,expenses_by_month):
        for expense in expenses_by_month:
            for row in range(len(self.transactions_table.get_children())):
                row_values = self.transactions_table.item(row)['values']
                if self.get_day_from_date(expense.get_expense_date()) == str(row_values[2]):
                    row_with_new_expense = row_values
                    index = self.expense_columns[self.get_expense_name_by_id(expense.get_expense_type())]

                    row_with_new_expense[index] += expense.get_expense_amount()

                    self.transactions_table.item(row, text="", values=row_with_new_expense)

    """ Method that adds the buttons to the transactions table"""
    def create_and_pack_buttons(self):
        new_income_button = Button(self, text="New Income", command="")
        new_expense_button = Button(self, text="New Expense", command="")
        new_income_button.pack()
        new_expense_button.pack()

    @staticmethod
    def get_day_from_date(date):
        split = date.split('-')[2]
        if split[0] == '0':
            return split[1]

        return split

    def get_expense_name_by_id(self,expense_id):
        for expense_type in self.expense_types:
            if expense_type.get_id() == expense_id:
                return expense_type.get_name()
        return None

    def get_expense_type_names(self):
        names = []
        for expense in self.expense_types:
            names.append(expense.get_name())
        return names

    def callback(self,*clicked):
        print(f"The variable has changed to '{self.clicked_month.get()}'")
        self.update_transactions_table()

    def update_transactions_table(self):
        self.transactions_table.destroy()
        self.transactions_table = ttk.Treeview(self)
        self.build_transactions_table()
        self.data_to_transactions_table_by_month(
            self.months[self.clicked_month.get()])
        self.transactions_table.pack()
