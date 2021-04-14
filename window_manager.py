import tkinter as tk

from tkinter import Toplevel
from services import Services as serve
import global_constants as glob_const

class WindowManager:
    LARGE_FONT = ("Verdana", 12)
    NORM_FONT = ("Helvetica", 10)
    SMALL_FONT = ("Helvetica", 8)

    def __init__(self):
        self.root = tk.Tk()
        self.service = serve()
        self.is_logged_in = False
        self.login_message = glob_const.NEED_LOGIN
        self.menu_bar = tk.Menu(self.root)
        self.customize_menu()
        # self.main_window_title = main_title
        # self.main_window_size = size
        # self.main_window = self.create_main_window(self.main_window_title,self.main_window_size)


    def customize_menu(self):
        self.root.config(menu=self.menu_bar)
        file_menu = tk.Menu(self.menu_bar,tearoff=0)
        pocket_menu = tk.Menu(self.menu_bar,tearoff=0)
        cards_menu = tk.Menu(self.menu_bar,tearoff=0)

        self.menu_bar.add_cascade(label="File",menu=file_menu)
        self.menu_bar.add_cascade(label="Pockets",menu=pocket_menu)
        self.menu_bar.add_cascade(label="Credit Cards",menu=cards_menu)

        file_menu.add_command(label="New Account", command=self.root.quit)
        file_menu.add_command(label="Edit Accounts", command=self.root.quit)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.root.quit)

        pocket_menu.add_command(label="New Pocket")
        pocket_menu.add_command(label="Edit or Delete Pocket")
        pocket_menu.add_command(label="Transfer to Pockets")

        cards_menu.add_command(label="New Credit Card")
        cards_menu.add_command(label="Edit Credit Card")
        cards_menu.add_command(label="View Movements")

    def verify_login(self, username, password):

        self.service.verify_user_for_login(username, password)
        if self.service.is_logged_in:
            popup.grab_release()
            popup.destroy()
        else:
            message_label.config(text = glob_const.WRONG_USER_OR_PASSWORD)

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
                                  command=lambda:self.verify_login(username_entry.get(),password_entry.get()))
        cancel_login_button = tk.Button(popup, text="Cancel",
                                  command=self.root.quit)
        log_in_button.pack()
        cancel_login_button.pack()