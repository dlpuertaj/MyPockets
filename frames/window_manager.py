import tkinter as tk

from tkinter import ttk
from tkinter import Toplevel
from services import Services as serve
import global_constants as glob_const


class WindowManager:
    LARGE_FONT = ("Verdana", 12)
    NORM_FONT = ("Helvetica", 10)
    SMALL_FONT = ("Helvetica", 8)

    def __init__(self):
        self.root = tk.Tk()
        self.serve = serve()
        self.is_logged_in = False
        self.login_message = glob_const.NEED_LOGIN
        self.menu_bar = tk.Menu(self.root)
        self.customize_menu()
        self.pocket_frame = tk.Frame(self.root)
        self.resume_frame = tk.Frame(self.root)
        self.pockets_table = ttk.Treeview(self.pocket_frame)
        self.customize_main_frame()
        self.build_pocket_table()
        self.list_box = tk.Listbox()

    def customize_menu(self):
        self.root.config(menu=self.menu_bar)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        pocket_menu = tk.Menu(self.menu_bar, tearoff=0)
        cards_menu = tk.Menu(self.menu_bar, tearoff=0)

        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.menu_bar.add_cascade(label="Pockets", menu=pocket_menu)
        self.menu_bar.add_cascade(label="Credit Cards", menu=cards_menu)

        file_menu.add_command(label="New Account")
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.root.quit)

        pocket_menu.add_command(label="New Pocket")
        pocket_menu.add_command(label="Transfer to Pockets")

        cards_menu.add_command(label="New Credit Card")
        cards_menu.add_command(label="View Movements")

    def verify_login(self, username, password):

        self.service.verify_user_for_login(username, password)
        if self.service.is_logged_in:
            popup.grab_release()
            popup.destroy()
            self.build_main_frame()
        else:
            message_label.config(text=glob_const.WRONG_USER_OR_PASSWORD)

    def create_popup_login(self):
        global popup
        popup = Toplevel(self.root)
        popup.grab_set()
        popup.title("Log in")
        global message_label
        message_label = tk.Label(popup, text=self.login_message, font=self.NORM_FONT)
        username_label = tk.Label(popup, text="Username: ", font=self.NORM_FONT)
        username_label.pack(side="top", fill="x", pady=10)
        username_entry = tk.Entry(popup)
        username_entry.pack()
        password_label = tk.Label(popup, text="Password: ", font=self.NORM_FONT)
        password_label.pack(side="top", fill="x", pady=10)
        password_entry = tk.Entry(popup)
        password_entry.pack()
        message_label.pack(side="top", fill="x", pady=10)

        # TODO: Add empty entry error
        log_in_button = tk.Button(popup, text="Log in",
                                  command=lambda: self.verify_login(username_entry.get(), password_entry.get()))
        cancel_login_button = tk.Button(popup, text="Cancel",
                                        command=self.root.quit)
        log_in_button.pack()
        cancel_login_button.pack()

    def build_main_frame(self):
        self.customize_pocket_frame()
        self.build_pocket_table()
        self.add_pockets_to_table()
        self.customize_resume_frame()
        self.build_resume_table()
        self.add_resume_data_to_table()

    def customize_pocket_frame(self):
        new_income_button = tk.Button(self.pocket_frame, text="New Income",
                                      command="")
        new_expense_button = tk.Button(self.pocket_frame, text="New Expense",
                                       command="")
        new_income_button.pack()
        new_expense_button.pack()
        self.pocket_frame.pack(side="left", fill=tk.BOTH, expand=1)

    def build_pocket_table(self):

        self.pockets_table['columns'] = ("Name", "Amount")
        self.pockets_table.heading("0", text="", anchor=tk.W)
        self.pockets_table.column("#0", width=0, stretch=tk.NO)

        self.pockets_table.column("Name", anchor=tk.W, width=100)
        self.pockets_table.column("Amount", anchor=tk.W, width=100)

        self.pockets_table.heading("Name", text="Name", anchor=tk.W)
        self.pockets_table.heading("Amount", text="Amount", anchor=tk.W)

    def customize_resume_frame(self):
        expense_types = serve.get_expense_types()
        self.resume_frame.pack(side="right", fill=tk.BOTH, expand=1)


    def build_resume_table(self):
        resume_table = ttk.Treeview(self.resume_frame)
        resume_table['columns'] = ("Income", "Day", "Type", "Note")

        resume_table.column("#0", width=0, stretch=tk.NO)
        resume_table.column("Income", anchor=tk.W, width=100)
        resume_table.column("Day", anchor=tk.W, width=100)
        resume_table.column("Type", anchor=tk.W, width=100)
        resume_table.column("Note", anchor=tk.W, width=100)

        resume_table.heading("0", text="", anchor=tk.W)
        resume_table.heading("Income", text="Income", anchor=tk.W)
        resume_table.heading("Day", text="Day", anchor=tk.W)
        resume_table.heading("Type", text="Type", anchor=tk.W)
        resume_table.heading("Note", text="Amount", anchor=tk.W)
        resume_table.pack()

    def load_pockets_to_tables(self):
        iid = 0
        pockets_data = self.serve.get_pockets()
        for pocket in pockets_data:
            self.pockets_table.insert(parent='', index='end', iid=iid, text="Parent", values=(pocket[1], pocket[2]))
            iid = iid + 1
        self.pockets_table.pack()

    def show_income_frame(self):
        return None

    def show_expense_frame(self):
        return None
