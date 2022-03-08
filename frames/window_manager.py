import tkinter as tk

from tkinter import ttk

import global_constants
from entities.expense_event import ExpenseEvent
from entities.income_event import IncomeEvent
from frames.pocket_frame import PocketFrame
from frames.popup.pop_event import PopEvent
from frames.popup.pop_login import PopLogin
from frames.popup.pop_pocket import PopPocket
from frames.resume_frame import ResumeFrame
from frames.transactions_frame import TransactionsFrame
from services import Services as serve


class WindowManager:
    """  Method that initializes  the window manager
         It calls the method that builds the menu bar.
         It initializes the Notebook.
         It initializes the pocket frame, the resume frame and the transactions frame.
         It also initializes the tables for the pocket info and the resume of the month.
         Lastly depending on a global property, it shows the popup for the login.
         """
    is_logged_in = False
    login_message = global_constants.NEED_LOGIN_MESSAGE
    __QUIT = 'Quit'

    def __init__(self):
        self.root = tk.Tk()
        self.serve = serve()
        self.menu_bar = tk.Menu(self.root)
        self.pockets = None
        self.pocket_frame    = PocketFrame(self.root)
        self.pockets_table   = ttk.Treeview(self.pocket_frame)
        self.resume_notebook = ttk.Notebook(self.root)
        self.resume_frame    = ResumeFrame(self.resume_notebook)
        self.resume_table    = ttk.Treeview(self.resume_frame)
        self.transactions_frame = TransactionsFrame(self.resume_notebook)
        self.create_menu_bar()

        self.ask_for_login()

    def ask_for_login(self):
        if global_constants.REQUIRES_LOGIN:
            self.login()
        else:
            self.build_main_frame()

    def login(self):
        """ Method that creates and shows the popup for the user login."""
        pop_login = PopLogin(self.root, self.serve)
        self.root.wait_window(pop_login)
        self.build_main_frame()

    def build_main_frame(self):
        """ Method that calls the creation of the pocket frame and the resume frame.
            It also adds the resume frame and the transactions frame to the Notebook """
        initial_month = '01' # TODO: get current month
        self.pockets = self.load_pockets()
        self.pocket_frame.create_pocket_frame()
        self.resume_frame.create_resume_frame()
        self.transactions_frame.create_transaction_frame(initial_month)
        self.resume_notebook.add(self.resume_frame, text=global_constants.EXPENSE_RESUME_TEXT)
        self.resume_notebook.add(self.transactions_frame, text=global_constants.MONTHLY_TRANSACTIONS_TEXT)
        self.resume_notebook.pack()

    def load_pockets(self):
        return self.serve.get_pockets()

    def add_menu_to_menu_bar(self, new_menu, label_for_new_menu):
        self.menu_bar.add_cascade(label=label_for_new_menu,menu=new_menu)

    def create_menu_bar(self):
        """ Method that creates the menu bar. """
        self.root.config(menu=self.menu_bar)

        file_menu   = tk.Menu(self.menu_bar, tearoff=0)
        pocket_menu = tk.Menu(self.menu_bar, tearoff=0)
        cards_menu  = tk.Menu(self.menu_bar, tearoff=0)

        self.add_menu_to_menu_bar(file_menu  , global_constants.FILE_MENU)
        self.add_menu_to_menu_bar(pocket_menu, global_constants.POCKETS_MENU)
        self.add_menu_to_menu_bar(cards_menu , global_constants.CREDIT_CARDS_MENU)

        file_menu.add_command(label=global_constants.NEW_INCOME_LABEL,
                              command=lambda: self.new_event(IncomeEvent(None,None,None,"","")))
        file_menu.add_command(label=global_constants.NEW_EXPENSE_LABEL,
                              command=lambda: self.new_event(ExpenseEvent(None,None,None,"","")))
        file_menu.add_separator()

        file_menu.add_command(label=global_constants.NEW_EXPENSE_TYPE_LABEL,
                              command=lambda: self.resume_frame.create_type(True))
        file_menu.add_command(label=global_constants.NEW_INCOME_TYPE_LABEL,
                              command=lambda: self.resume_frame.create_type(False))

        file_menu.add_separator()
        file_menu.add_command(label=self.__QUIT, command=self.root.quit)

        pocket_menu.add_command(label=global_constants.NEW_POCKET,command=self.new_pocket)
        # pocket_menu.add_command(label="Transfer to Pockets")

        # cards_menu.add_command(label="New Credit Card")
        # cards_menu.add_command(label="View Movements")

    """ Method that shows a popup for the creation of a new expense event"""
    def new_event(self, event_type):
        if len(self.pockets) == 0:
            serve.show_popup_message(self.root, "No pockets created")
        else:
            pop_event = PopEvent(self.root,event_type)
            pop_event.create_and_show_popup(self.serve)
            self.root.wait_window(pop_event)
            self.update_tables()

    def update_tables(self):
        self.resume_frame.update_resume_table()
        self.transactions_frame.update_transactions_table()
        self.update_pockets_table()

    def update_pockets_table(self):
        self.pocket_frame.update_pockets_table()
        self.load_pockets()

    def new_pocket(self):
        pop_new_pocket = PopPocket(self.root)
        pop_new_pocket.create_and_show_popup(self.serve)
        self.root.wait_window(pop_new_pocket)
        self.update_pockets_table()
