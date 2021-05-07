from tkinter import Toplevel, Label, Entry, Button
import global_constants as glob_const


class PopLogin(Toplevel):
    LARGE_FONT = ("Verdana", 12)
    NORM_FONT = ("Helvetica", 10)
    SMALL_FONT = ("Helvetica", 8)

    def __init__(self, root):
        Toplevel.__init__(root)
        self.grab_set()
        self.title("Log in")
        self.login_message_label = Label(self, text=glob_const.NEED_LOGIN, font=self.NORM_FONT)
        self.username_label = Label(self, text="Username: ", font=self.NORM_FONT)
        self.username_entry = Entry(self)
        self.password_label = Label(self, text="Password: ", font=self.NORM_FONT)
        self.password_entry = Entry(self)

    def create_popup_login(self):
        self.username_label.pack(side="top", fill="x", pady=10)

        self.username_entry.pack()

        self.password_label.pack(side="top", fill="x", pady=10)

        self.password_entry.pack()

        self.login_message_label.pack(side="top", fill="x", pady=10)

        # TODO: Add empty entry error
        log_in_button = Button(self, text="Log in",
                               command=lambda: self.verify_login(self.username_entry.get(), self.password_entry.get()))
        cancel_login_button = Button(self, text="Cancel", command=self.root.quit)
        log_in_button.pack()
        cancel_login_button.pack()
