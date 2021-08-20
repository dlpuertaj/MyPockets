from tkinter import Frame, W, NO, BOTH, StringVar, Label, OptionMenu
from tkinter import ttk

from services import Services as serve


class ResumeFrame(Frame):

    """ Iit method that instantiates service and resume table"""
    def __init__(self,root):
        Frame.__init__(self,root)
        self.resume_table = ttk.Treeview(self)
        self.serve = serve()
        self.clicked_month = None

    """ Method that creates the resume frame and loads the data from the database"""
    def create_resume_frame(self):
        self.create_select_month_option_menu()
        self.build_resume_table()
        self.load_resume_data_to_table()
        self.pack(side="right", fill=BOTH, expand=1)

    """ Method that builds the resume table adding the columns and the headers"""
    def build_resume_table(self):
        columns = []

        expense_types = self.serve.get_expense_type_names()
        for expense_type in expense_types:
            columns.append(expense_type[0])

        self.resume_table['columns'] = columns
        self.resume_table.heading("0", text="", anchor=W)
        self.resume_table.column("#0", width=0, stretch=NO)

        for column in columns:
            self.resume_table.column(column, anchor=W, width=100)

        for column in columns:
            self.resume_table.heading(column, text=column, anchor=W)

    def create_select_month_option_menu(self):
        months = ['01','02','03','04','05','06','07','08','09','10','11','12']
        self.clicked_month = StringVar()
        self.clicked_month.set(months[0])
        self.clicked_month.trace("w",self.callback)
        type_label = Label(self, text="Month")
        type_label.pack()
        dropdown = OptionMenu(self, self.clicked_month, *months)
        dropdown.pack()

    """ Method that adds the database data to the resume table"""
    def load_resume_data_to_table(self):
        resume_data = self.serve.get_resume_data((self.clicked_month.get(),))
        payroll = self.serve.get_payroll_by_month((self.clicked_month.get(),))

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

    def callback(self,*clicked):
        print(f"the variable has changed to '{self.clicked_month.get()}'")
        self.resume_table = ttk.Treeview(self)
        self.resume_table.destroy()
        self.build_resume_table()
        self.load_resume_data_to_table()