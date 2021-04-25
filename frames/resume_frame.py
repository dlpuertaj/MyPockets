from tkinter import Frame, BOTH, ttk,W,NO
from services import Services as serve

class ResumeFrame(Frame):

    def __init__(self):
        super(ResumeFrame,self).__init__()
        self.serve = serve()
        self.resume_table = ttk.Treeview(self)

    def create_resume_frame(self):
        self.build_resume_table()
        self.load_resume_data_to_table()
        self.pack(side="right", fill=BOTH, expand=1)

    def build_resume_table(self):
        columns = []

        expense_types = self.serve.get_expense_types()
        for expense_type in expense_types:
            columns.append(expense_type[0])

        self.resume_table['columns'] = columns
        self.resume_table.heading("0", text="", anchor=W)
        self.resume_table.column("#0", width=0, stretch=NO)

        for column in columns:
            self.resume_table.column(column, anchor=W, width=100)

        for column in columns:
            self.resume_table.heading(column, text=column, anchor=W)

    def load_resume_data_to_table(self):
        resume_data = self.serve.get_resume_data(('04',))
        payroll = self.serve.get_payroll_by_month(('04',))

        amount_for_table = []
        percent_for_table = []
        sum_percent = 0
        for data in resume_data:
            percent = data[1]/payroll[0]
            amount_for_table.append(data[1])
            percent_for_table.append(str(percent*100)+"%")
            sum_percent += percent

        self.resume_table.insert(parent='', index='end', iid=0, text="Parent", values=amount_for_table)

        self.resume_table.insert(parent='', index='end', iid=1, text="Parent", values=percent_for_table)

        self.resume_table.pack()
