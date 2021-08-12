from tkinter import Toplevel, Button, Label, Entry, OptionMenu, StringVar
from services import Services as srv

""" Generic popup for error, alert or any message"""
class PopupGenericMessage(Toplevel):

    def __init__(self, root,message):
        Toplevel.__init__(self,root)
        self.root = root
        self.serve = srv()
        self.message = message
        self.show_popup()

    def show_popup(self):
        message_label = Label(self, text=self.message)
        close_button = Button(self, text="Cancel", command=self.destroy)
        message_label.pack()
        close_button.pack()
