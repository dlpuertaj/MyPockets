import tkinter as tk

from tkinter import ttk
from tkinter import Toplevel

from frames.pocket_frame import PocketFrame
from frames.resume_frame import ResumeFrame
from frames.transactions_frame import TransactionsFrame
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
        self.resume_notebook = ttk.Notebook(self.root)
        self.pocket_frame = PocketFrame(self.root) #tk.Frame(self.root)
        self.resume_frame = ResumeFrame(self.resume_notebook)  # tk.Frame(self.resume_notebook)
        self.transactions_frame = TransactionsFrame(self.resume_notebook)
        self.pockets_table = ttk.Treeview(self.pocket_frame)
        self.resume_table = ttk.Treeview(self.resume_frame)

        if glob_const.PROP_REQUIRE_LOGIN:
            self.create_popup_login()
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
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.root.quit)

        pocket_menu.add_command(label="New Pocket")
        pocket_menu.add_command(label="Transfer to Pockets")

        cards_menu.add_command(label="New Credit Card")
        cards_menu.add_command(label="View Movements")

    def verify_login(self, username, password):
        self.serve.verify_user_for_login(username, password)
        if self.serve.is_logged_in:
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
        self.pocket_frame.create_pocket_frame()
        self.resume_frame.create_resume_frame()
        self.transactions_frame.create_transaction_frame('04')
        self.resume_notebook.pack()
        self.resume_notebook.add(self.resume_frame, text="Expense Resume")
        self.resume_notebook.add(self.transactions_frame, text="Monthly Transactions")

    def show_income_frame(self):
        return None

    def show_expense_frame(self):
        return None
