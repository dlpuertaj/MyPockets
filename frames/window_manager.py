import tkinter as tk

from tkinter import ttk

from frames.pocket_frame import PocketFrame
from frames.popup.pop_expense_event import PopExpense
from frames.popup.pop_login import PopLogin
from frames.resume_frame import ResumeFrame
from frames.transactions_frame import TransactionsFrame
from services import Services as serve
import global_constants as glob_const


class WindowManager:

    def __init__(self):
        self.root = tk.Tk()
        self.serve = serve()
        self.is_logged_in = False
        self.login_message = glob_const.NEED_LOGIN
        self.menu_bar = tk.Menu(self.root)
        self.customize_menu()
        self.resume_notebook = ttk.Notebook(self.root)
        self.pocket_frame = PocketFrame(self.root)  # tk.Frame(self.root)
        self.resume_frame = ResumeFrame(self.resume_notebook)  # tk.Frame(self.resume_notebook)
        self.transactions_frame = TransactionsFrame(self.resume_notebook)
        self.pockets_table = ttk.Treeview(self.pocket_frame)
        self.resume_table = ttk.Treeview(self.resume_frame)

        if glob_const.PROP_REQUIRE_LOGIN:
            self.login()
        else:
            self.build_main_frame()

    def customize_menu(self):
        self.root.config(menu=self.menu_bar)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        pocket_menu = tk.Menu(self.menu_bar, tearoff=0)
        cards_menu = tk.Menu(self.menu_bar, tearoff=0)

        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.menu_bar.add_cascade(label="Pockets", menu=pocket_menu)
        self.menu_bar.add_cascade(label="Credit Cards", menu=cards_menu)

        file_menu.add_command(label="New Account")
        file_menu.add_command(label="New Expense", command=self.new_expense_event)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.root.quit)

        pocket_menu.add_command(label="New Pocket")
        pocket_menu.add_command(label="Transfer to Pockets")

        cards_menu.add_command(label="New Credit Card")
        cards_menu.add_command(label="View Movements")

    def login(self):
        pop_login = PopLogin(self.root, self.serve)
        self.root.wait_window(pop_login)
        self.build_main_frame()

    def build_main_frame(self):
        self.pocket_frame.create_pocket_frame()
        self.resume_frame.create_resume_frame()
        self.transactions_frame.create_transaction_frame('04')
        self.resume_notebook.pack()
        self.resume_notebook.add(self.resume_frame, text="Expense Resume")
        self.resume_notebook.add(self.transactions_frame, text="Monthly Transactions")

    def new_expense_event(self):
        pop_expense_event = PopExpense(self.root,None)
        pop_expense_event.create_and_show_popup()
        self.root.wait_window(pop_expense_event)
        # TODO: update everything

    def show_expense_frame(self):
        return None
