from tkinter import Frame, W, NO, BOTH, Button, Label
from tkinter import ttk

from services import Services as serve


class ResumeFrame(Frame):

    """ Iit method that instantiates service and resume table"""
    def __init__(self,root):
        Frame.__init__(self,root)
        self.resume_table = ttk.Treeview(self)
        self.serve = serve()
        # self.clicked_month = None

    """ Method that creates the resume frame and loads the data from the database"""
    def create_resume_frame(self):
        # self.create_select_month_option_menu()
        expense_types = self.serve.get_expense_type_names()
        if len(expense_types) > 0:
            self.build_resume_table()
            self.load_resume_data_to_table()
        else:
            no_expense_types_label = Label(self,text="No expense type created")
            no_expense_types_label.pack()
            new_expense_type_button = Button(self,text="Create Expense Type",
                                             command=self.create_expense_type)
            new_expense_type_button.pack()
        self.pack(side="right", fill=BOTH, expand=1)

    def create_expense_type(self):
        pass

    """ Method that builds the resume table adding the columns and the headers"""
    def build_resume_table(self,expense_types):
        columns = []

        for expense_type in expense_types:
            columns.append(expense_type[0])

        self.resume_table['columns'] = columns
        self.resume_table.heading("0", text="", anchor=W)
        self.resume_table.column("#0", width=0, stretch=NO)

        for column in columns:
            self.resume_table.column(column, anchor=W, width=100)

        for column in columns:
            self.resume_table.heading(column, text=column, anchor=W)

    """ Method that adds the database data to the resume table"""
    def load_resume_data_to_table(self):
        expense_types = self.serve.get_expense_type_names()
        resume_data = self.serve.get_resume_data(('01',))
        payroll = self.serve.get_payroll_by_month(('01',))

        amount_for_table = []
        percent_for_table = []
        sum_percent = 0

        if len(resume_data) == 0:
            resume_data = ('None',0)
        for data in resume_data:

            for column_index in range(len(expense_types)):
                column = self.resume_table.column(column_index,option='id')
                if data[0] == column:
                    if payroll == 0:
                        percent = 0
                    else:
                        percent = data[1]/payroll[0]
                    amount_for_table.append(data[1])
                    percent_for_table.append(str(percent*100)+"%")
                    sum_percent += percent
                else:
                    amount_for_table.append(0)
                    percent_for_table.append("0%")
                    sum_percent += 0

        self.resume_table.insert(parent='', index='end', iid=0, text="Parent", values=amount_for_table)

        self.resume_table.insert(parent='', index='end', iid=1, text="Parent", values=percent_for_table)

        self.resume_table.pack()

    def update_resume_table(self):
        self.resume_table.destroy()
        self.resume_table = ttk.Treeview(self)
        self.build_resume_table()
        self.load_resume_data_to_table()
