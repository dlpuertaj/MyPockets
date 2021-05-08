from tkinter import Toplevel, Label, Entry, Button
import global_constants as glob_const
from services import Services as serve


class PopLogin(Toplevel):
    LARGE_FONT = ("Verdana", 12)
    NORM_FONT = ("Helvetica", 10)
    SMALL_FONT = ("Helvetica", 8)

    def __init__(self, root,service):
        self.root = root
        Toplevel.__init__(self,root)
        self.serve = service
        self.grab_set()
        self.title("Log in")
        self.login_message_label = Label(self, text=glob_const.NEED_LOGIN, font=self.NORM_FONT)
        self.username_label = Label(self, text="Username: ", font=self.NORM_FONT)
        self.username_entry = Entry(self)
        self.password_label = Label(self, text="Password: ", font=self.NORM_FONT)
        self.password_entry = Entry(self)
        self.show_popup_login()

    def show_popup_login(self):
        self.username_label.pack(side="top", fill="x", pady=10)
        self.username_entry.pack()
        self.password_label.pack(side="top", fill="x", pady=10)
        self.password_entry.pack()
        self.login_message_label.pack(side="top", fill="x", pady=10)

        # TODO: Add empty entry error
        log_in_button = Button(self, text="Log in",
                               command=lambda: self.login(self.username_entry.get(), self.password_entry.get()))
        cancel_login_button = Button(self, text="Cancel", command=self.root.quit)
        log_in_button.pack()
        cancel_login_button.pack()

    def login(self,username,password):
        self.serve.verify_user_for_login(username, password)
        if self.serve.is_logged_in:
            self.grab_release()
            self.destroy()
        else:
            self.login_message_label.config(text=glob_const.WRONG_USER_OR_PASSWORD)
