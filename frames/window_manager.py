import tkinter as tk

from tkinter import ttk

import global_constants
from entities.expense_event import ExpenseEvent
from entities.income_event import IncomeEvent
from frames.pocket_frame import PocketFrame
from frames.popup.pop_event import PopEvent
from frames.popup.pop_login import PopLogin
from frames.popup.pop_new_type import PopNewType
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

    pockets = None
    expense_types = None
    income_types = None

    def __init__(self):
        self.root = tk.Tk()
        self.serve = serve()
        self.load_pockets_and_types()

        self.resume_notebook    = ttk.Notebook(self.root)
        self.transactions_frame = TransactionsFrame(self.resume_notebook,self.expense_types)
        self.resume_frame       = ResumeFrame(self.resume_notebook,self.expense_types)
        self.resume_table       = ttk.Treeview(self.resume_frame)

        self.pocket_frame       = PocketFrame(self.root,self.pockets)
        self.pockets_table      = ttk.Treeview(self.pocket_frame)

        self.menu_bar           = tk.Menu(self.root)
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

    def load_pockets_and_types(self):
        self.pockets = self.serve.get_pockets()
        self.income_types = self.serve.get_income_types()
        self.expense_types = self.serve.get_expense_types()

    def build_main_frame(self):
        """ Method that calls the creation of the pocket frame and the resume frame.
            It also adds the resume frame and the transactions frame to the Notebook """
        initial_month = '01' # TODO: get current month
        self.pocket_frame.create_pocket_frame()
        self.resume_frame.create_resume_frame()
        self.transactions_frame.create_transaction_frame(initial_month)
        self.resume_notebook.add(self.resume_frame, text=global_constants.EXPENSE_RESUME_TEXT)
        self.resume_notebook.add(self.transactions_frame, text=global_constants.MONTHLY_TRANSACTIONS_TEXT)
        self.resume_notebook.pack()

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

    def create_type(self, expense_or_income):
        pop_new_type = PopNewType(self.root, expense_or_income)
        pop_new_type.create_and_show_popup(self.serve)
        self.root.wait_window(pop_new_type)
        self.update_tables()
        self.load_types()

    """ Method that shows a popup for the creation of a new expense event"""
    def new_event(self, event_type):
        if len(self.pockets) == 0:
            serve.show_popup_message(self.root, "No pockets created")
        else:
            if self.event_options_in_database(event_type):
                pop_event = PopEvent(self.root,event_type)
                pop_event.create_and_show_popup(self.serve,self.pockets)
                self.root.wait_window(pop_event)
                self.update_tables()
                self.load_types()
            else:
                self.load_types()
                if self.event_options_in_database(event_type):
                    pop_event = PopEvent(self.root, event_type)
                    pop_event.create_and_show_popup(self.serve, self.pockets)
                    self.root.wait_window(pop_event)
                    self.update_tables()
                    self.load_types()
                else:
                    serve.show_popup_message(self.root, "No type created")

    def update_tables(self):
        self.resume_frame.update_resume_table()
        self.transactions_frame.update_transactions_table()
        self.update_pockets_table()

    def update_pockets_table(self):
        self.pockets = self.serve.get_pockets()
        self.pocket_frame.set_pockets(self.pockets)
        self.pocket_frame.update_pockets_table()

    def new_pocket(self):
        pop_new_pocket = PopPocket(self.root)
        pop_new_pocket.create_and_show_popup(self.serve)
        self.root.wait_window(pop_new_pocket)
        self.update_pockets_table()

    def event_options_in_database(self, event_type):
        type_of_event = str(type(event_type))
        if "income" in type_of_event:
            return len(self.income_types) > 0
        else:
            return len(self.expense_types) > 0
