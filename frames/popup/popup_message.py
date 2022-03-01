from tkinter import Toplevel, Button, Label, Entry, OptionMenu, StringVar

""" Generic popup for error, alert or any message"""
class PopupGenericMessage(Toplevel):

    def __init__(self, root,message):
        Toplevel.__init__(self,root)
        self.root = root
        self.message = message
        self.show_popup()

    def show_popup(self):
        message_label = Label(self, text=self.message)
        close_button = Button(self, text="Ok", command=self.destroy)
        message_label.pack()
        close_button.pack()
