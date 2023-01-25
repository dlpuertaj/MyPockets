import ttkbootstrap as ttkboot
from tkinter import Toplevel, Label, Entry, Button

from ttkbootstrap import PRIMARY, DANGER

from util import global_constants as glob_const
from services import data_services

class PopLogin(ttkboot.Toplevel):
    LARGE_FONT = ("Verdana", 12)
    NORM_FONT = ("Helvetica", 10)
    SMALL_FONT = ("Helvetica", 8)

    """ Init method that initializes the login popup and it's components"""
    def __init__(self, root,db):
        self.root = root
        self.db_connection = db
        Toplevel.__init__(self,root)
        self.title("Log in")
        self.login_message_label = ttkboot.Label(self, text=glob_const.NEED_LOGIN_MESSAGE, font=self.NORM_FONT)
        self.username_label = ttkboot.Label(self, text="Username: ", font=self.NORM_FONT)
        self.username_entry = ttkboot.Entry(self)
        self.password_label = ttkboot.Label(self, text="Password: ", font=self.NORM_FONT)
        self.password_entry = ttkboot.Entry(self)
        self.grab_set()

        self.show_popup_login()

    """ Method that shows the popup for the user login"""
    def show_popup_login(self):
        self.username_label.grid(column="0", row="0")
        self.username_entry.grid(column="1", row="0")
        self.password_label.grid(column="0", row="1")
        self.password_entry.grid(column="1", row="1")
        self.login_message_label.grid(column="0", row="2", columnspan="2")

        # TODO: Add empty entry error
        log_in_button = ttkboot.Button(self, text="Log in",
                                       bootstyle=PRIMARY,
                                       command=lambda: self.login(self.username_entry.get(), self.password_entry.get()))
        cancel_login_button = ttkboot.Button(self, text="Cancel", bootstyle=DANGER, command=self.root.quit())
        log_in_button.grid(column="0", row="3")
        cancel_login_button.grid(column="1",row="3")

    """ Method that executes the validation of the information entered by the user for the login"""
    def login(self,username,password):
        user_found = data_services.verify_user_for_login(self.db_connection, username, password)
        if user_found is not None:
            self.grab_release()
            self.destroy()
        else:
            self.login_message_label.config(text=glob_const.WRONG_USER_OR_PASSWORD)
