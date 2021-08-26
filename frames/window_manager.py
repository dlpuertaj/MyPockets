import tkinter as tk

from tkinter import ttk

from frames.pocket_frame import PocketFrame
from frames.popup.pop_event import PopEvent
from frames.popup.pop_login import PopLogin
from frames.resume_frame import ResumeFrame
from frames.transactions_frame import TransactionsFrame
from services import Services as serve
import global_constants as glob_const


class WindowManager:

    """  Method that initializes  the window manager
         It calls the method that builds the menu bar.
         It initializes the Notebook.
         It initializes the pocket frame, the resume frame and the transactions frame.
         It also initializes the tables for the pocket info and the resume of the month.
         Lastly depending on a global property, it shows the popup for the login.
         """
    def __init__(self):
        self.root = tk.Tk()
        self.serve = serve()
        self.is_logged_in = False
        self.login_message = glob_const.NEED_LOGIN
        self.menu_bar = tk.Menu(self.root)
        self.customize_menu() # menú superior
        self.pocket_frame = PocketFrame(self.root)  # tk.Frame(self.root)
        self.pockets_table = ttk.Treeview(self.pocket_frame)
        self.resume_notebook = ttk.Notebook(self.root)
        self.resume_frame = ResumeFrame(self.resume_notebook)  # tk.Frame(self.resume_notebook)
        self.resume_table = ttk.Treeview(self.resume_frame)
        self.transactions_frame = TransactionsFrame(self.resume_notebook)

        if glob_const.PROP_REQUIRE_LOGIN:
            self.login()
        else:
            self.build_main_frame()

    """ Method that builds the menu bar. """
    def customize_menu(self):
        self.root.config(menu=self.menu_bar)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        pocket_menu = tk.Menu(self.menu_bar, tearoff=0)
        cards_menu = tk.Menu(self.menu_bar, tearoff=0)

        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.menu_bar.add_cascade(label="Pockets", menu=pocket_menu)
        self.menu_bar.add_cascade(label="Credit Cards", menu=cards_menu)

        file_menu.add_command(label="New Account") #TODO: create command method
        file_menu.add_command(label="New Income", command=lambda: self.new_event(True))
        file_menu.add_command(label="New Expense", command=lambda: self.new_event(False))
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.root.quit)

        # pocket_menu.add_command(label="New Pocket")
        # pocket_menu.add_command(label="Transfer to Pockets")

        # cards_menu.add_command(label="New Credit Card")
        # cards_menu.add_command(label="View Movements")

    """ Method that creates and shows the popup for the user login."""
    def login(self):
        pop_login = PopLogin(self.root, self.serve)
        self.root.wait_window(pop_login)
        self.build_main_frame()

    """ Method that calls the creation of the pocket frame and the resume frame.
        It also adds the resume frame and the transactions frame to the Notebook """
    def build_main_frame(self):
        self.pocket_frame.create_pocket_frame()
        self.resume_frame.create_resume_frame()
        self.transactions_frame.create_transaction_frame('04')
        self.resume_notebook.pack()
        self.resume_notebook.add(self.resume_frame, text="Expense Resume")
        self.resume_notebook.add(self.transactions_frame, text="Monthly Transactions")

    """ Method that shows a popup for the creation of a new expense event"""
    def new_event(self, event_type):
        pop_event = PopEvent(self.root,event_type,None)
        pop_event.create_and_show_popup()
        self.root.wait_window(pop_event)
        self.update_tables()

    def update_tables(self):
        self.resume_frame.update_resume_table()