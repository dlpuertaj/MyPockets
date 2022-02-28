from tkinter import Toplevel, Button, Label, Entry, OptionMenu, StringVar
from datetime import date
import global_constants
from frames.popup.popup_message import PopupGenericMessage


class PopPocket(Toplevel):
    """ Class that creates the popup for creating, updating or deleting a pocket"""

    def __init__(self,root):
        Toplevel.__init__(self,root)
        self.root = root
        self.grab_set()

    def create_and_show_popup(self,serve):

        pocket_name_label = Label(self,text="Name: ")
        pocket_name_entry = Entry(self)

        save_button = Button(self, text="Save", command=lambda:
                             self.save_pocket(serve,pocket_name_entry.get()))

        close_button = Button(self, text="Close", command=self.destroy)

        pocket_name_label.pack()
        pocket_name_entry.pack()

        save_button.pack()
        close_button.pack()

    def save_pocket(self, serve, pocket_name):
        pass