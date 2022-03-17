from tkinter import Frame, W, NO, BOTH, Button, Label
from tkinter import ttk

from frames.popup.pop_new_type import PopNewType
from services import Services as serve

import calendar as calendar

class ResumeFrame(Frame):
    """ Iit method that instantiates service and resume table"""

    months = ("01","02","03","04","05","06",
              "07","08","09","10","11","12")

    def __init__(self, root, expense_types):
        Frame.__init__(self, root)
        self.serve = serve()
        self.root = root
        self.clicked_month = None
        self.resume_tables = []
        self.expense_types = expense_types
        self.no_expense_types_label = Label(self, text="No expense type created")
        self.new_expense_type_button = Button(self, text="Create Expense Type",
                                              command=lambda: self.create_type(True))

    """ Method that creates the resume frame and loads the data from the database"""

    def create_resume_frame(self):
        # self.create_select_month_option_menu()
        #expense_types = self.serve.get_expense_type_names()
        for month in self.months:
            if len(self.expense_types) > 0:
                resume_table = self.build_resume_table(self.expense_types)

                month_label = Label(self,text=calendar.month_name[int(month)])
                self.load_resume_data_to_table(resume_table,month,month_label)
                self.resume_tables.append(resume_table)
            else:
                self.no_expense_types_label.pack()
                self.new_expense_type_button.pack()
            self.pack(side="right", fill=BOTH, expand=1)

    """ Method that builds the resume table adding the columns and the headers"""

    def build_resume_table(self, expense_types):
        columns = []
        resume_table = ttk.Treeview(self,height=2)
        for expense_type in expense_types:
            columns.append(expense_type.get_name())

        resume_table['columns'] = columns
        resume_table.heading("0", text="", anchor=W)
        resume_table.column("#0", width=0, stretch=NO)

        for column in columns:
            resume_table.column(column, anchor=W, width=100)

        for column in columns:
            resume_table.heading(column, text=column, anchor=W)

        return resume_table

    """ Method that adds the database data to the resume table"""
    def load_resume_data_to_table(self,resume_table,month,month_label):
        #expense_types = self.serve.get_expense_type_names()
        resume_data = self.serve.get_resume_data((month,))
        payroll = self.serve.get_payroll_by_month((month,))

        amount_for_table = []
        percent_for_table = []
        sum_percent = 0

        it_has_data = False
        if resume_data[0][0] != 'None':
            it_has_data = True

        for data in resume_data:
            for column_index in range(len(self.expense_types)):
                column = resume_table.column(column_index, option='id')
                if data[0] == column:
                    if payroll == 0:
                        percent = 0
                    else:
                        percent = data[1] / payroll[0]
                        percent = round(percent,4)
                    amount_for_table.append(data[1])
                    percent_for_table.append(str(percent * 100) + "%")
                    sum_percent += percent
                else:
                    amount_for_table.append(0)
                    percent_for_table.append("0%")
                    sum_percent += 0

        resume_table.insert(parent='', index='end', iid=0, text="Parent", values=amount_for_table)

        resume_table.insert(parent='', index='end', iid=1, text="Parent", values=percent_for_table)

        if it_has_data:
            month_label.pack()
            resume_table.pack()

    def create_type(self, expense_or_income):
        pop_new_type = PopNewType(self.root, expense_or_income)
        pop_new_type.create_and_show_popup(self.serve)
        self.root.wait_window(pop_new_type)
        self.update_resume_table()

    def update_resume_table(self):
        self.expense_types = self.serve.get_expense_type_names()
        if len(self.expense_types) > 0:
            self.no_expense_types_label.destroy()
            self.new_expense_type_button.destroy()
        resume_table = self.build_resume_table(self.expense_types)
        self.load_resume_data_to_table(resume_table)
        resume_table.pack()

